from src.li.Li import Li
from src import router

class SourceLi(Li):
    def __init__(self, source, collectionFile, sourceVisual):
        title = sourceVisual.title(source)   
        icon, thumb = sourceVisual.images(source)          
              
        url = router.browseSourceUrl(source.id, collectionFile)
        
        isFolder = True
        isPlayable = False
            
        generalInfoLabels = None
        videoInfoLabels = None
 
    
        super(SourceLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels)