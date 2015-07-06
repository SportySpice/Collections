from src.videosource.VideoSource import VideoSource, SourceType
from src.videosource.VideoList import VideoList
from Thumb import Thumb
import settings as s
from YoutubeVideo import YoutubeVideo
from src.paths.root import PLAYLIST_CACHE_DIR
from src.file import File
import service
from datetime import datetime
from Pages import Pages, ItemType, TimeUnit
from src import router


CACHE_FILE_EXTENSION = '.pla'


playlistsLoaded = {}


class Playlist(VideoSource):
    def __init__(self, playlistId, cacheFile, channelSource=None):
        if channelSource:
            self.playlistId = playlistId
            self.videoSource = channelSource
            self.videos = Pages(self._videosRequest, self._videosResponseProcess, ItemType.VIDEO, 'channel upload playlist videos', s.videosCacheTime, TimeUnit.MINUTES, channelSource)
            return
            
        
        
        self.playlistId = playlistId
        self.videoSource = self
        self.videos = None
        self.videoCount = 0
        self._gotInfo = False
        
        
        
        if cacheFile is None:
            raise ValueError('Playlist constructor must receive cachefile, this proves the loaded tried to first loading the instance from cache')
        self.cacheFile = cacheFile 
        
                
        
                
        global playlistsLoaded
        if self.playlistId in playlistsLoaded:            
            raise ValueError('Playlist is in memory but with a different instance. This should never happen.')
        else:            
            playlistsLoaded[self.playlistId] = self
        
        
        
        
        
        
    #must be called at least once before making any use of the object (unless it has a channel source)        
    def updateInfo(self, snippet, videoCount=None, updatedInfoAt=datetime.now()):                    
        title = snippet['title']
        channelTitle = snippet['channelTitle']
        studioTitle = channelTitle
        tvShowTitle = title
                
        description = snippet ['description']
    
        youtubeThumb = Thumb(snippet['thumbnails'])
        thumb = youtubeThumb.get(s.sourceThumbres)
        #self.youtubeThumb = youtubeThumb
        
        sourceType = SourceType.PLAYLIST
        sourceId = self.playlistId
             
        super(Playlist, self).__init__(title, studioTitle, tvShowTitle, description, thumb, sourceType, sourceId)
        
        
        if videoCount:
            self.videoCount = videoCount
                        
        
        if self.videos is None:
            self.videos = Pages(self._videosRequest, self._videosResponseProcess, ItemType.VIDEO, 'playlist videos', s.videosCacheTime, TimeUnit.MINUTES, self)
        
        
        
        self._gotInfo = True
        self._updatedInfoAt = updatedInfoAt
        
        self.cache()


        
####################
## Private Methods##
####################      
    def _playlistInfoRequest(self):
        request = service.service().playlists().list(part="snippet,contentDetails", id=self.playlistId)
        return request
    
    
    
    
    def _processPlaylistInfoResposne(self, response):
        items = response.get("items", [])
        if len(items) != 1:        
            raise ValueError('Playlist list request by single playlistId should return exactly 1 result. Returned: %s \nplaylistId: %s' % (len(items), self.playlistId))
        
        item = items[0]
        snippet = item['snippet']
        videoCount = item['contentDetails']['itemCount']
        return snippet, videoCount
    
    
    
    def _processBatchPlaylistInfoResponse(self, request_id, response, exception):
        if exception:
            raise ValueError('Exception thrown in playlist info request from batch. \nRequest ID: {0}. Playlist ID: {1}. \nException: {2}'.format(request_id, self.playlistId, exception))
        
        snippet, videoCount = self._processPlaylistInfoResposne(response)        
        return snippet, videoCount
        

    
    def _videosRequest(self, pageToken):
            return service.service().playlistItems().list(part="snippet,status", playlistId=self.playlistId, maxResults=50, pageToken=pageToken)
            
    def _videosResponseProcess(self, response):
        self.videoSource.videoCount = response['pageInfo']["totalResults"]
        
        
        
        videos = VideoList()
        
        items = response.get("items", [])
                       
        position = 1
        for item in items:
            privacyStatus = item['status']['privacyStatus'] 
            snippet = item['snippet']
            videoId = snippet['resourceId']['videoId']
            
            if  privacyStatus == 'public':
                video = YoutubeVideo(self.videoSource, position, snippet)
                videos.append(video)                
                position += 1     
                
            elif privacyStatus=='private':                
                print 'Private video, skipping! (%s)' %videoId
            else:
                raise ValueError('Unknown video privacy status: %s. videoId: %s \nSnippet: %s' %(privacyStatus, videoId, snippet))
            
        return videos

               
        
        
        
####################
## Public Methods##
#################### 
    ##override (unused currently)
    def fetchInfo(self):
        if self.videoSource != self:
            raise ValueError ('Upload playlist belonging to a channel should never fetch its own info, something went wrong here!')
        
        request = self._playlistInfoRequest()
        response = request.execute()        
        snippet, videoCount = self._processPlaylistInfoResposne(response)
                                    
        self.updateInfo(snippet, videoCount)        


    #override
    def fetchInfoBatchRequest(self):
        if self.videoSource != self:
            raise ValueError ('Upload playlist belonging to a channel should never fetch its own info, something went wrong here!')
        
        request = self._playlistInfoRequest()
        
        def callback(request_id, response, exception):
            snippet, videoCount = self._processBatchPlaylistInfoResponse(request_id, response, exception)  
            self.updateInfo(snippet, videoCount)



        return (request, callback)
    
    
    #override
    def needsInfoUpdate(self):
        if not self._gotInfo:
            return True
        
        timePassed = datetime.now() - self._updatedInfoAt        
        if timePassed.seconds > s.sourceInfoCacheTime()*86400:
            return True
        
        return False
    
    

            
    

    


    def cache(self):
        self.cacheFile.dumpObject(self)
        





    def browseUrl(self, pageNum=1):
        return router.browseYoutubePlaylistUrl(self.cacheFile, pageNum)
  
    



      
#     
# def fromBatchInfoRequest(playlistId, sourceCallback):
#     request = Playlist._playlistInfoRequest(playlistId)
#     
#     def callback(request_id, response, exception):
#         snippet = Playlist._processBatchPlaylistInfoRequest(request_id, response, exception, playlistId)
#         playlist = Playlist(playlistId, snippet)
#         
#         sourceCallback(playlist)
#             
# 
#     return (request, callback)




def fromCacheFile(cacheFile):
    playlist = cacheFile.loadObject()
    
    global playlistsLoaded
    if playlist.playlistId in playlistsLoaded:
        raise ValueError("Tried loading playlist from cache when it's already in memory")
    playlistsLoaded[playlist.playlistId] = playlist
    
    return playlist




def _fromMemoryOrCache(playlistId):
    global playlistsLoaded

    if playlistId in playlistsLoaded:
        return playlistsLoaded[playlistId], None
        
    cacheFileName = playlistId + CACHE_FILE_EXTENSION
    cacheFile = File.fromNameAndDir(cacheFileName, PLAYLIST_CACHE_DIR)
        
    if cacheFile.exists():
        playlist = fromCacheFile(cacheFile)        
        return playlist, None
    
    return None, cacheFile




def fromPlaylistId(playlistId):
    playlist, cacheFile = _fromMemoryOrCache(playlistId)
    if not playlist:
        playlist = Playlist(playlistId, cacheFile)
        
    if playlist.needsInfoUpdate():
        needsInfoUpdate = True
    else:
        needsInfoUpdate = False
    
    return playlist, needsInfoUpdate








def _fromSnippet(playlistId, snippet, videoCount=None):
    playlist, cacheFile = _fromMemoryOrCache(playlistId)
    if not playlist:
        playlist = Playlist(playlistId, cacheFile)
        
    playlist.updateInfo(snippet, videoCount)
    return playlist
    




    


def fromPlaylistsRequest(item):
    playlistId = item['id']
    snippet = item['snippet']
    videoCount = item['contentDetails']['itemCount']
     
    return _fromSnippet(playlistId, snippet, videoCount)



def fromSearchRequest(item):
    playlistId = item['id']['playlistId']
    snippet = item['snippet']
    
    return _fromSnippet(playlistId, snippet)