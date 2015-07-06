import FeedTextSettings
import globalCollection
from src.li.visual.ViewStyle import ViewStyle
from src.videosource.Video import OnVideoClick
from src.videosource.VideoList import VideoSort, VideoCountType





D_VIEWSTYLE = ViewStyle.EPISODES
D_SORT  = VideoSort.DATE
D_SORT2 = None
D_REVERSE_SORT = False
D_COUNT_TYPE    = VideoCountType.DATE
D_COUNT_TYPE2   = VideoCountType.VIEWS
#D_REPLACE_VIEWS = True
D_VIDEOCLICK = OnVideoClick.PLAY_QUEUE_REST
D_UNWATCHED = False
D_LIMIT = 50
D_SLIMIT = 20
D_USE = False
D_USELIMITS = False


MAX_LIMIT = 50   #google doesn't allow more than 50 items per request, will require multiple requests


gfs = None        
class FeedSettings(object):
    def __init__(self, viewStyle, videoSort, videoSort2, reverseSort, vCountType, vCountType2, onVideoClick, unwatched, limit, sLimit, use, useLimits, feedTS):
        self._viewStyle = viewStyle        
        self._sort = videoSort
        self._sort2 = videoSort2
        self._reverseSort = reverseSort
        self._countType = vCountType
        self._countType2 = vCountType2
        #self._replaceViews = replaceViews
        self._onVideoClick = onVideoClick
        self._unwatched = unwatched        
        self._limit = limit
        self.sLimit = sLimit if sLimit<=MAX_LIMIT else MAX_LIMIT
        
                
        self.use = use
        self.useLimits = useLimits
        self.TS = feedTS
        feedTS.setFs(self)
        
        
 
    def viewStyle(self):        return self._viewStyle      if self.use     else gfs.viewStyle()        
    def onVideoClick(self):     return self._onVideoClick   if self.use     else gfs.onVideoClick()    
    def sort(self):             return self._sort           if self.use     else gfs.sort()
    def sort2(self):            return self._sort2          if self.use     else gfs.sort2()
    def reverseSort(self):      return self._reverseSort    if self.use     else gfs.reverseSort()
    def countType(self):        return self._countType      if self.use     else gfs.countType()
    def countType2(self):       return self._countType2     if self.use     else gfs.countType2()
#     def replaceViews(self):     return self._replaceViews   if self.use     else gfs.replaceViews()    
    def unwatched(self):        return self._unwatched      if self.use     else gfs.unwatched()
        
    def limit(self):            return self._limit          if self.useLimits     else gfs.limit()
    
    def showSettings(self):     return self.TS.settingsTS().show
    def showSort(self):         return self.TS.sortTS().show
    def showPlayAll(self):      return self.TS.playAllTS().show    
       
         
    def playVideoOnly(self):    return True  if self.onVideoClick() == OnVideoClick.PLAY_ONLY else False
        
        
    #     def sLimit(self): #         return self._sLimit if self.use else gfs.sLimit()
    
    
    def setViewStyle(self, viewStyle):          self._viewStyle = viewStyle        
    def setSort(self, videoSort):               self._sort = videoSort        
    def setSort2(self, videoSort):              self._sort2 = videoSort
    def setReverseSort(self, state):            self._reverseSort = state
    def setCountType(self, vCountType):         self._countType = vCountType
    def setCountType2(self, vCountType):        self._countType2 = vCountType        
#     def setReplaceViews(self, state):           self._replaceViews = state    
    def setOnVideoClick(self, onVideoClick):    self._onVideoClick = onVideoClick    
    def setUnwatched(self, state):              self._unwatched = state        
    def setLimit(self, value):                  self._limit = value        
    def setSourceLimit(self, value):            self.sLimit = value        
    def setUse(self, state):                    self.use = state
    def setUseLimits(self, state):              self.useLimits = state
        



def init():
    global gfs
    
    if gfs is None:
        gc = globalCollection.gc()
        gfs = gc.feedSettings

    
    
def default():
    feedTS = FeedTextSettings.default()
    return FeedSettings(D_VIEWSTYLE, D_SORT, D_SORT2, D_REVERSE_SORT, D_COUNT_TYPE, D_COUNT_TYPE2, D_VIDEOCLICK, 
                        D_UNWATCHED, D_LIMIT, D_SLIMIT, D_USE, D_USELIMITS, feedTS)