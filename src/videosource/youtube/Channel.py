from src.videosource.VideoSource import VideoSource, SourceType
import Playlist
import service
from Thumb import Thumb
import settings as s
from src.paths.root import CHANNEL_CACHE_DIR
from src.file import File
from datetime import datetime
from Pages import Pages, ItemType, TimeUnit
from src.tools import DataDictionary
from src import router


USERNAME_DIC_FILE = '__usernames.dic'
CACHE_FILE_EXTENSION = '.cha'
 
 
 
channelsLoaded = {}


class Channel(VideoSource):
    def __init__(self, channelId=None, username=None):
        self.username = username
        self.channelId = channelId 
            
        self._uploadPlaylist = None
        self.playlists = None
        self._gotInfo = False
        
        self.viewCount = None
        self.commentCount = None
        self.subscriberCount = None
        self.videoCount = None
        





    #must be called at least once before making any use of the object        
    def updateInfo(self, snippet, channelId, contentDetails=None, statistics=None, videoCount=None, subNewItemCount=None, updatedInfoAt=datetime.now()):
        title = snippet['title']        
        studioTitle = title
        tvShowTitle = '%s Uploads' %title
        
        description = snippet['description']
        
        youtubeThumb = Thumb(snippet['thumbnails'])
        thumb = youtubeThumb.get(s.sourceThumbres)
        #self.youtubeThumb = youtubeThumb
        
           
        sourceType = SourceType.CHANNEL
        sourceId = channelId
        
        super(Channel, self).__init__(title, studioTitle, tvShowTitle, description, thumb, sourceType, sourceId)
        
        
        
        self.channelId = channelId        
        cacheFileName = self.channelId + CACHE_FILE_EXTENSION
        self.cacheFile = File.fromNameAndDir(cacheFileName, CHANNEL_CACHE_DIR)
         
        
        
        
        
        
        
        if self.username:
            usernameDic = DataDictionary.load(USERNAME_DIC_FILE, CHANNEL_CACHE_DIR)
            usernameDic.setIfNonExistent(self.username, channelId)
        
        
        if contentDetails:
            playlistId = contentDetails['relatedPlaylists']['uploads']
             
            if (self._uploadPlaylist is None) or (self._uploadPlaylist and self._uploadPlaylist.playlistId != playlistId):
                self._uploadPlaylist = Playlist.Playlist(playlistId, None, channelSource=self)
                self.videos = self._uploadPlaylist.videos
                #self._uploadPlaylist.fetchInfo()
                
        if statistics:
            self.viewCount = int(statistics['viewCount'])
            self.commentCount = int(statistics['commentCount'])
            self.subscriberCount = int(statistics['subscriberCount'])
            if statistics['videoCount'] != 0:
                self.videoCount = int(statistics['videoCount'])
            
        if videoCount and videoCount!=0:
            self.videoCount = videoCount
            
        if subNewItemCount:
            self.subNewItemCount = subNewItemCount      #this is for subscription channels
          
 
        if self.playlists is None:
            self.playlists = Pages(self._playlistsRequest, self. _playlistsResponseProcesse, ItemType.VSOURCE, 'channel playlists', s.channelPlaylistsCacheTime, TimeUnit.DAYS, self)
        


        
        
        
        global channelsLoaded
        if self.channelId in channelsLoaded:
            if channelsLoaded[self.channelId] != self:
                raise ValueError('Channel is in memory but with a different instance. This should never happen.')
        else:            
            channelsLoaded[self.channelId] = self
        
        
        self._gotInfo = True
        self._updatedInfoAt = updatedInfoAt
        
        self.cache()
        
        
        
        
        
###################
## Public Methods##
###################
    #override
    def fetchInfo(self):
        request = self._channelInfoRequest()
        response = request.execute()        
        channelId, snippet, contentDetails, statistics = self._processChannelInfoResposne(response)
        
        self.updateInfo(snippet, channelId, contentDetails, statistics)
    
    
    #override
    def fetchInfoBatchRequest(self):
        request = self._channelInfoRequest()
        
        def callback(request_id, response, exception):
            channelId, snippet, contentDetails, statistics = self._processBatchChannelInfoResponse(request_id, response, exception)  
            self.updateInfo(snippet, channelId, contentDetails, statistics)



        return (request, callback)
    
    
    #override
    def needsInfoUpdate(self, checkUploadPlaylist=False):
        if checkUploadPlaylist and self.needPlaylistInfo():
            return True
        
        if not self._gotInfo:
            return True
        
        
        timePassed = datetime.now() - self._updatedInfoAt        
        if timePassed.seconds > s.sourceInfoCacheTime()*86400:
            return True
        
        
        return False
            
            
    
    def needPlaylistInfo(self):
        if not self._uploadPlaylist:
            return True
        
        return False
    
    
    
    
    def cache(self, fromPages=False):
        if fromPages:
            self.cacheFile.dumpObject(self)
            return
        
        self.playlists.enterCachedModeAndCacheSourceObject()
        
        
        



####################
## Private Methods##
####################
    def _channelInfoRequest(self):
        request = service.service().channels().list(part = "contentDetails,snippet,statistics", forUsername=None if self.channelId else self.username, id=self.channelId)
        return request 
        
    
    def _processChannelInfoResposne(self, response):
        items = response.get("items", [])
        if len(items) != 1:
            raise ValueError('Channel list request by username or id should return exactly 1 result. Returned: %s \nusername: %s. channelId:%s' % (len(items), self.username, self.channelId))
        
        item = items[0]
        
        
        return Channel._processChannelInfoItem(item)
     
    @staticmethod
    def _processChannelInfoItem(item): 
        channelId = item['id']
        snippet = item['snippet']
        contentDetails = item['contentDetails']
        statistics = item['statistics']
        
        return channelId, snippet, contentDetails, statistics
    
    
    def _processBatchChannelInfoResponse(self, request_id, response, exception):
        if exception:            
            raise ValueError('Exception thrown in channel info request from batch. \nRequest ID: {0}. Channel username: {1}. Channel ID: {2} \nException: {3}'.format(request_id, self.username, self.channelId, exception))
        
        channelId, snippet, contentDetails, statistics = self._processChannelInfoResposne(response)
        return channelId, snippet, contentDetails, statistics
    
    
    def _playlistsRequest(self, pageToken):
        return service.service().playlists().list(channelId=self.channelId, part='snippet,contentDetails', maxResults=50, pageToken=pageToken)
    
    def _playlistsResponseProcesse(self, response):
        playlists = []
    
        for item in response['items']:
            playlist = Playlist.fromPlaylistsRequest(item)            
            playlists.append(playlist)
        
        return playlists



    def browseUrl(self, pageNum=1):
        return router.browseYoutubeChannelUrl(self.cacheFile, pageNum)
    



# 
# def fromBatchInfoRequest(username=None, channelId=None, sourceCallback):        
#     request = Channel._channelInfoRequest(username, channelId)
#     
#     def callback(request_id, response, exception):
#         channelId, snippet, contentDetails = Channel._processBatchChannelInfoResponse(request_id, response, exception, username, channelId)  
#         channel = Channel(snippet, channelId, username, contentDetails)
#         
#         sourceCallback(channel)
#             
#     return (request, callback)







def fromCacheFile(cacheFile):
    global channelsLoaded 
    
    channel = cacheFile.loadObject()
    channel.playlists.loadFromCachedMode()
    
    if channel.channelId in channelsLoaded:
        raise ValueError("Tried loading channel from cache when it's already in memory")
    channelsLoaded[channel.channelId] = channel
    
    
    return channel





def _fromMemoryOrCache(channelId=None, username=None):
    global channelsLoaded
    
    if username is None and channelId is None:
        raise ValueError('Channel loader must get either username or channelId. Got neither.')
    
    if username and not channelId:
        usernameDic = DataDictionary.load(USERNAME_DIC_FILE, CHANNEL_CACHE_DIR)
        if not usernameDic.has(username):
            return None
        
        channelId = usernameDic.get(username)
        
            
    
    if channelId in channelsLoaded:
        return channelsLoaded[channelId]
    
    
    
    cacheFileName = channelId + CACHE_FILE_EXTENSION
    cacheFile = File.fromNameAndDir(cacheFileName, CHANNEL_CACHE_DIR)
        
    if cacheFile.exists():
        channel = fromCacheFile(cacheFile)        
        return channel
    
    return None
        
        
        

def fromUserOrId(channelId=None, username=None):
    channel = _fromMemoryOrCache(channelId, username)
    if not channel:
        channel = Channel(channelId, username)
        
    if channel.needsInfoUpdate():
        needsInfoUpdate = True
    else:
        needsInfoUpdate = False
    
    return channel, needsInfoUpdate
        
        
        
        
        
        

def _fromSnippet(channelId, snippet, contentDetails=None, statistics=None, videoCount=None, subNewItemCount=None):
    channel = _fromMemoryOrCache(channelId)
    if not channel:
        channel = Channel(channelId=channelId)
    
    channel.updateInfo(snippet, channelId, contentDetails, statistics, videoCount, subNewItemCount)    
    return channel

    
    
    
    
def fromChannelsRequest(item):
    channelId, snippet, contentDetails, statistics = Channel._processChannelInfoItem(item)        
    return _fromSnippet(channelId, snippet, contentDetails, statistics)
    





def fromSearchRequest(item):
    channelId = item['id']['channelId']     
    snippet = item['snippet']
    #username = snippet['channelTitle']    #maybe use later, make sure is correct (not positive)
     
    return _fromSnippet(channelId, snippet)      #incomplete info, need to call fetchlInfo if channel not found in cache
    



def fromSubscriptionsRequest(item):
    channelId = item['snippet']['resourceId']['channelId']
    snippet = item['snippet']
    videoCount = int(item['contentDetails']['totalItemCount'])
    newItemCount = item['contentDetails']['newItemCount']
    
    if videoCount == 0:
        videoCount = None 

    return _fromSnippet(channelId, snippet, videoCount=videoCount, subNewItemCount=newItemCount)        #incomplete info, need to call fetchInfo if channel not found in cache