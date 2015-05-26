from src.collection.Source import Source
from Thumb import Thumb
from Video import Video
import service


class Playlist(Source):
    def __init__(self, playlistId, sourceSettings, source=None):
        super(Playlist, self).__init__(sourceSettings)
        self.videoList = None
        self.id = playlistId                    
        self.source = source        
        
####################
## Private Methods##
####################                    
    def _processInitialResponse(self, response):
        apiItems = response.get("items", [])
        if len(apiItems) != 1:            
            raise ValueError('playlist info request should return exactly 1 result. Returned: %s' % len(apiItems))
        
        apiPlaylist = apiItems[0]
        apiSnippet = apiPlaylist['snippet']
        
        self.title = apiSnippet['title']
        self.title2 = self.title
        self.description = apiSnippet ['description']
        self.thumb = Thumb(apiSnippet['thumbnails'])
        
        
        
    def _processUpdateResponse(self, response, unlimitedList=False):
        videoList = []            
        
        playListItems = response.get("items", [])        
        
        position = 1
        for playlistItem in playListItems:
            snippet = playlistItem['snippet']
            
            if 'thumbnails' in snippet:
                if self.source is not None:
                    source = self.source
                else:
                    source = self
                video = Video(snippet, position=position, source=source)
                videoList.append(video)                
                position += 1     
            else:
                title = snippet['title']
                description = snippet['description']
                videoId = snippet['resourceId']['videoId']
                
                if (title == 'Private video' and description == 'This video is private.'):
                    print 'Private video, skipping! (%s)' %videoId
                elif (title == 'Deleted video' and description == 'This video is unavailable.'):
                    print 'Deleted video, skipping! (%s)' %videoId
                else:
                    raise ValueError('no thumbnails in video for unknown reason. video id: %s. \nSnippet: %s' %(videoId, snippet))    
        
        if unlimitedList:
            self.unlimitedVideoList = videoList
        else:
            self.videoList = videoList
        
        
        
        
####################
## Public Methods##
#################### 
    #override         
    def getInitialRequest(self):
        request = service.service().playlists().list(part = "snippet", id=self.id)
        
        def callback(request_id, response, exception):
            if exception is not None:
                raise ValueError(str.format('Exception thrown in initial playlist info http request from batch. \nRequest ID: {0}. Playlist ID: {1}. \nException: {2}', request_id, self.id, exception))
            else:
                self._processInitialResponse(response)
                

        return (request, callback)
        
        
    #override 
    def getUpdateRequest(self):
        request = service.service().playlistItems().list(part="snippet", playlistId=self.id, maxResults=self.limit)
        
        def callback(request_id, response, exception):
            if exception is not None:
                raise ValueError('Exception thrown in update playlist videos http request from batch. Request ID: %s \nException: %s' %(request_id,exception))
            else:
                self._processUpdateResponse(response)
                
        return (request, callback)
    

    #override    
    def videos(self):
        return self.videoList
    
    
    #override
    def updateUnlimitedVideos(self):
        request = service.service().playlistItems().list(part="snippet", playlistId=self.id, maxResults=50)        
        response = request.execute()
        self._processUpdateResponse(response, unlimitedList=True)
                
    #override  
    def unlimitedVideos(self):
        return self.unlimitedVideoList
             
             
                            
    ##works but currently unused
    #def updateInitialInfo(self):
    #    request = service.service.playlists().list(part = "snippet", id=self.id)
    #    response = request.execute()
    #    self.processInitialInfoResponse(response)           