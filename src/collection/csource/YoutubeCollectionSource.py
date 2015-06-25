from src.collection.CollectionSource import CollectionSource
from src.collection.settings import globalCollection

gss = None
class YoutubeCollectionSource(CollectionSource):
    def __init__(self, index, collection, vSourceYT, onClick=None, limit=None, customTitle=None, customThumb=None):
        super(YoutubeCollectionSource, self).__init__(index, collection, vSourceYT, onClick, limit, customTitle, customThumb)
        
    
    def videosNeedUpdate(self):
        return self.videoSource.videos.pageNeedsUpdate(pageNum=1)
    
    
    def updateVideosBatchRequest(self):
        return self.videoSource.videos.updatePageBatchRequest(pageNum=1)
    
    def allVideos(self):
        return self.videoSource.videos.pageItems(pageNum=1)
    
    
    def onClick(self):
        if not self.css.use:
            return gss.onSourceClickYt
                        
        return self._onClick if self._onClick else self.css.onSourceClickYt
    
    
    
    
    
    
def init():
    global gss
    gss = globalCollection.gc().sourcesSettings