import FeedTextSettings
import globalCollection
from src.li.visual.ViewStyle import ViewStyle
from src.videosource.Video import OnVideoClick


D_VIEWSTYLE = ViewStyle.EPISODES
D_VIDEOCLICK = OnVideoClick.PLAY_QUEUE_REST
D_UNWATCHED = False
D_LIMIT = 50
D_SLIMIT = 20
D_USE = False


MAX_LIMIT = 50   #google doesn't allow more than 50 items per request, will require multiple requests


gfs = None        
class FeedSettings(object):
    def __init__(self, viewStyle, onVideoClick, unwatched, limit, sLimit, use, feedTS):
        self._viewStyle = viewStyle
        self._onVideoClick = onVideoClick
        self._unwatched = unwatched        
        self._limit = limit
        self.sLimit = sLimit if sLimit<=MAX_LIMIT else MAX_LIMIT
        
                
        self.use = use
        self.TS = feedTS
        
 
    def viewStyle(self):
        return self._viewStyle if self.use else gfs.viewStyle()
        
    def onVideoClick(self): 
        return self._onVideoClick if self.use else gfs.onVideoClick()
    
    def unwatched(self):
        return self._unwatched if self.use else gfs.unwatched()
    
    def limit(self): 
        return self._limit if self.use else gfs.limit()
    
#     def sLimit(self): 
#         return self._sLimit if self.use else gfs.sLimit() 



    def showPlayAll(self):
        return self.TS.playAllTS().show
    
    def showSettings(self):
        return self.TS.settingsTS().show
    
    def playVideoOnly(self):
        if self.onVideoClick() == OnVideoClick.PLAY_ONLY:
            return True
        
        return False
    
    
    def setViewStyle(self, viewStyle):
        self._viewStyle = viewStyle
    
    def setOnVideoClick(self, onVideoClick):
        self._onVideoClick = onVideoClick
    
    def setUnwatched(self, state):
        self._unwatched = state
        
    def setLimit(self, value):
        self._limit = value
        
    def setSourceLimit(self, value):
        self.sLimit = value
        
    def setUse(self, state):
        self.use = state
        



def init():
    global gfs
    
    if gfs is None:
        gc = globalCollection.gc()
        gfs = gc.feedSettings

    
    
def default():
    feedTS = FeedTextSettings.default()
    return FeedSettings(D_VIEWSTYLE, D_VIDEOCLICK, D_UNWATCHED, D_LIMIT, D_SLIMIT, D_USE, feedTS)