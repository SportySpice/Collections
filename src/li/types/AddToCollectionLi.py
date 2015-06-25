from src.li.Li import Li
from src import router

class AddToCollectionLi(Li):
    def __init__(self, vSource, addToCollectionVisual):
        title = addToCollectionVisual.title()   
        icon, thumb = addToCollectionVisual.images()          
        
        url = router.addToCollectionUrl(vSource.id, vSource.cacheFile, vSource.type)
        
        isFolder = False
        isPlayable = False
            
        generalInfoLabels = None
        videoInfoLabels = None
 
    
        super(AddToCollectionLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels)