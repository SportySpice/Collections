import globalCollection
from src.li.visual.TextSettings import TextSettings
from src.tools import addonSettings as addon


                            #color         #bold    #italic
D_CSOURCE = TextSettings    (None,          False,   False)
D_USE = False

FEED_TEXT = addon.string(440)


gsTS = None
class SourcesTextSettings(object):
    def __init__(self, cSourceTS, use):
        self._cSourceTS = cSourceTS            
        self.use = use
        
        
    def cSourceTS(self):
        return self._cSourceTS if self.use else gsTS.cSourceTS()
    
    



    def setCSource(self, TS):
        self._cSourceTS = TS
        
    def setUse(self, state):
        self.use = state
    

def init():
    global gsTS
    
    if gsTS is None:
        gc = globalCollection.gc()
        gsTS = gc.sourcesSettings.TS
    

    
    
def default():
    return SourcesTextSettings(D_CSOURCE, D_USE)