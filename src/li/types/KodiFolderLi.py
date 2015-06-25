from src.li.Li import Li
from src import router

class KodiFolderLi(Li):
    def __init__(self, kodiFolder, kodiFolderVisual, root=False):
        title = kodiFolderVisual.title(kodiFolder)   
        
        icon = kodiFolder.thumb
        thumb = None
        
        url = router.browseKodiFolderUrl(kodiFolder.cacheFile, root)
        
        isFolder = True
        isPlayable = False
            
        generalInfoLabels = None
        videoInfoLabels = None
 
    
        super(KodiFolderLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels)