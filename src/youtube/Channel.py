from src.collection.Source import Source
from Playlist import Playlist
from Thumb import Thumb
import service

class Channel(Source):
    def __init__(self, sourceSettings, username=None, channelId=None):
        super(Channel, self).__init__(sourceSettings)
        self.uploadPlaylist = None
        self.username = username
        self.id = channelId
        


####################
## Private Methods##
####################     
        
    def _processInitialResponse(self, response):
        apiItems = response.get("items", [])
        if len(apiItems) != 1:
            raise ValueError('channel info by username or id  request should return exactly 1 result. Returned: %s \nusername: %s. channelId:%s' % (len(apiItems), self.username, self.id))

        apiChannel = apiItems[0]
        apiSnippet = apiChannel['snippet']
        apiContentDetails = apiChannel['contentDetails']
        
        

        self.title = apiSnippet['title']
        self.title2 = '%s Uploads' %self.title
        self.description = apiSnippet['description']
        self.id = apiChannel['id']
        self.thumb = Thumb(apiSnippet['thumbnails'])

        self.uploadPlaylist = Playlist(apiContentDetails['relatedPlaylists']['uploads'], self.sourceSettings, source=self)
        #self.uploadPlaylist.getInitialInfo()
        
        
        
        
        
###################
## Public Methods##
###################
    #override  
    def getInitialRequest(self):        
        request = service.service().channels().list(part = "contentDetails,snippet", forUsername=self.username, id=self.id)
        
        def callback(request_id, response, exception):
            if exception is not None:            
                raise ValueError(str.format('Exception thrown in initial channel info http request from batch. \nRequest ID: {0}. Channel username: {1} \nException: {2}', request_id, self.username, exception))
            else:
                self._processInitialResponse(response)
                
        return (request, callback)
                
                
    #override    
    def getUpdateRequest(self):
        return self.uploadPlaylist.getUpdateRequest()
      
      
    #override  
    def videos(self):
        return self.uploadPlaylist.videos()
    
    
    
    
    
    #override
    def updateUnlimitedVideos(self):
        self.uploadPlaylist.updateUnlimitedVideos()
                
    #override  
    def unlimitedVideos(self):
        return self.uploadPlaylist.unlimitedVideos()
    
    
      
      
      
    ##works but currently unused
    #def updateInitialInfo(self):
    #    request = service.channels().list(part = "contentDetails,snippet", forUsername=self.username)
    #    response = request.execute()
    #    self.processInitialInfoResponse(response)  