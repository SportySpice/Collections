import globalCollection

D_ESTIMATE_DATES = True
D_USE = False

gfds = None   
class FolderSettings(object):
    def __init__(self, estimateDates, use):
        self.estimateDates = estimateDates
        self.use = use
        


    def setEstimateDates(self, state):
        self.estimateDates = state
        
    def setUse(self, state):
        self.use = state




def init():
    global gfds
    
    if gfds is None:
        gc = globalCollection.gc()
        gfds = gc.folderSettings

    
    
def default():    
    return FolderSettings(D_ESTIMATE_DATES, D_USE)