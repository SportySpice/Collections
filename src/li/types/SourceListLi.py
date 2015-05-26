from src.li.Li import Li
from src import router

class SourceListLi(Li):
    def __init__(self, collectionFile, sourceListVisual):
        
        
        title = sourceListVisual.title()
        icon, thumb = sourceListVisual.images() 
        
        url = router.listSourcesUrl(collectionFile)
        
        isFolder = True
        isPlayalbe = False

        generalInfoLabels = None
        videoInfoLabels = None
 
        
        
        super(SourceListLi, self).__init__(title, icon, thumb, url, isFolder, isPlayalbe,
                                       videoInfoLabels, generalInfoLabels)