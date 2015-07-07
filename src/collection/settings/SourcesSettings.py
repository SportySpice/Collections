import SourcesTextSettings
import globalCollection
from src.li.visual.ViewStyle import ViewStyle
from src.collection.CollectionSource import OnSourceClick 

D_VIEWSTYLE = ViewStyle.FILES
D_SOURCE_CLICK_KODI = OnSourceClick.BROWSE
D_SOURCE_CLICK_YT   = OnSourceClick.BROWSE
D_USE = False


gss = None
class SourcesSettings(object):
    def __init__(self, viewStyle, onSourceClickKodi, onSourceClickYt, use, sourcesTS):
        self._viewStyle = viewStyle
        self.onSourceClickKodi = onSourceClickKodi
        self.onSourceClickYt = onSourceClickYt
        
        
        self.use = use
        self.TS = sourcesTS

        
    def viewStyle(self):
        return self._viewStyle if self.use else gss.viewStyle()
    
    
#     def onSourceClickKodi(self): 
#         return self._onSourceClickKodi if self.use else gss.onSourceClickKodi()
#     
#     def onSourceClickYt(self): 
#         return self._onSourceClickYt if self.use else gss.onSourceClickYt()




    def setViewStyle(self, viewStyle):
        self._viewStyle = viewStyle
        
    def setSourceClickKodi(self, onSourceClick):
        self.onSourceClickKodi = onSourceClick
        
    def setSourceClickYt(self, onSourceClick):
        self.onSourceClickYt = onSourceClick
        
    def setUse(self, state):
        self.use = state



def init():
    global gss
    
    if gss is None:
        gc = globalCollection.gc()        
        gss = gc.sourcesSettings




def default():
    sourcesTS = SourcesTextSettings.default()
    return SourcesSettings(D_VIEWSTYLE, D_SOURCE_CLICK_KODI, D_SOURCE_CLICK_YT, D_USE, sourcesTS)


