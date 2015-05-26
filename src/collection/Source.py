class Source(object):
    def __init__(self, sourceSettings):
        self.title = None
        self.title2 = None              #used mostly for "TVShow Title"
        self.description = None
        self.id = None
        self.thumb = None
        
        self.sourceSettings =   sourceSettings        
        self.limit =            sourceSettings.limit
        self.maxRepeat =        sourceSettings.maxRepeat
        self.push =             sourceSettings.push
        
        

        
        
        
###################
## Public Methods##
###################  
    ## after this request the following fields have to be filled (if they werent already):
    ## title, title2, description, id, thumb
    ## also updateRequest must be able to work after this request
    #abstract
    def getInitialRequest(self):        
        return
    
    #abstract
    def getUpdateRequest(self):
        return

    #abstract
    def videos(self):
        return
    
    #abstract
    def updateUnlimitedVideos(self):
        return
    
    #abstract
    def UnlimitedVideos(self):
        return