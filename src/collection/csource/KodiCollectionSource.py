from src.collection.CollectionSource import CollectionSource
from src.collection.settings import globalCollection
from src.videosource.VideoList import VideoList
from src.videosource.kodi.FolderVideo import FolderVideo
from src.videosource.kodi.FolderVideo import ParseMethod



D_PARSE_METHOD = ParseMethod.NORMAL 

gss  = None
gfds = None
class KodiCollectionSource(CollectionSource):
    def __init__(self, index, collection, kodiFolder, parseMethod, estimateDates=None, onClick=None, useInFeed=True, limit=None, customTitle=None, customThumb=None):
        if customTitle is None:
            customTitle = kodiFolder.title
            
        if (customThumb is None) and kodiFolder.thumb:
            customThumb = kodiFolder.thumb
        
        super(KodiCollectionSource, self).__init__(index, collection, kodiFolder, onClick, useInFeed, limit, customTitle, customThumb)
        
        self.parseMethod = parseMethod
        self._estimateDates = estimateDates
        
        #methods
        self.browseOriginUrl = kodiFolder.browseOriginUrl
        
    
    def updateVideos(self, estimateDates=False):
        self.videoSource.updateContents(estimateDates)
        
    def updateVideosIfDated(self, estimateDates=False):
        self.videoSource.updateContentsIfDated(estimateDates)
        
        
    #override        
    def allVideos(self):
        kodiFolder = self.videoSource        
        if kodiFolder.isEmpty() or kodiFolder.updateFailed():
            return VideoList();
        
        if self.parseMethod != ParseMethod.NORMAL:
            position = 0
            folderVideos = VideoList()
            
            for folder in kodiFolder.folders():
                folderVideo = FolderVideo(kodiFolder, position, folder, self.parseMethod)
                folderVideos.append(folderVideo)
                position += 1
                 
            return folderVideos
            
        return kodiFolder.videos()
    
    
    
    def estimateDates(self):
        if not self.cfds.use:
            return gfds.estimateDates
        
        return self._estimateDates if self._estimateDates is not None   else self.cfds.estimateDates
    
    #override
    def browseUrl(self):
        return self.videoSource.browseUrl(estimateDates=self.estimateDates())
    
    #override
    def onClick(self):
        if not self.css.use:
            return gss.onSourceClickKodi
                        
        return self._onClick if self._onClick else self.css.onSourceClickKodi
        
    

        
    def setParseMethod(self, parseMethod):
        self.parseMethod = parseMethod

    def setEstimateDates(self, state):
        self._estimateDates = state
        
        
        
        
        
        




        
def init():
    global gss
    global gfds
    
    gc = globalCollection.gc()
    gss = gc.sourcesSettings
    gfds = gc.folderSettings