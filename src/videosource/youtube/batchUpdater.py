import threading
from apiclient.http import BatchHttpRequest

def infoUpdate(vSources, forceUpdate=False):
    batch = BatchHttpRequest()
    sourcesToUpdate = False
    
    for vSource in vSources:
        if forceUpdate or vSource.needsInfoUpdate():
            request, callback = vSource.fetchInfoBatchRequest()
            batch.add(request, callback=callback)
            
            sourcesToUpdate = True
        
        
    if sourcesToUpdate:
        batch.execute()
        
        
        
        
        
        
        
def videoUpdate(vSources, pages=1, forceUpdate=False, fetchVideoStats=True):
    
    channelsNeedingUpdate = []
    
    for vSource in vSources:
        if vSource.isChannel() and vSource.needsInfoUpdate(checkUploadPlaylist=True):
            channelsNeedingUpdate.append(vSource)
            
    infoUpdate(channelsNeedingUpdate, forceUpdate=True)
                
                
    
    videoPagesToUpdate = []
    
    
            
    for vSource in vSources:   
        videos = vSource.videos
        
        for pageNum in range(1, pages+1):
            if forceUpdate or videos.pageNeedsUpdate(pageNum):
                videoPagesToUpdate.append((videos, pageNum))


    if not videoPagesToUpdate:
        return
    
    pageUpdateBatch = BatchHttpRequest()
    for page in videoPagesToUpdate:
        videos, pageNum = page
        
        request, callback = videos.updatePageBatchRequest(pageNum)
        pageUpdateBatch.add(request, callback=callback)
        
    pageUpdateBatch.execute()
        
    
    
    if fetchVideoStats:
        videoStatsBatch = BatchHttpRequest()
        for page in videoPagesToUpdate:
            videos, pageNum = page
        
            request, callback = videos.fetchVideoStatsBatchRequest(pageNum)
            videoStatsBatch.add(request, callback=callback)
        
        videoStatsBatch.execute()
        
        
            
#                                     
#                 videosToUpdate = True



    
    
    
        
    
def videoUpdateThread(vSources, pages=1, forceUpdate=False, fetchVideoStats=True):
        return VideoUpdater(vSources, pages, forceUpdate, fetchVideoStats)
    
    
class VideoUpdater(threading.Thread):
    def __init__(self, vSources, pages=1, forceUpdate=False, fetchVideoStats=True):
        threading.Thread.__init__(self)
        self.vSources = vSources
        self.pages = pages
        self.forceUpdate = forceUpdate
        self.fetchVideoStats = fetchVideoStats
        
    def run(self):
        videoUpdate(self.vSources, self.pages, self.forceUpdate, self.fetchVideoStats)