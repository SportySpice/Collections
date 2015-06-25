from src.li.Li import Li
from src import router

class CollectionSourcesLi(Li):
    def __init__(self, collection):
        title, icon, thumb = collection.feedSettings.TS.browseSourcesVisuals()        
        
        url = router.browseCollectionSourcesUrl(collection.file)
        
        isFolder = True
        isPlayalbe = False

        generalInfoLabels = None
        videoInfoLabels = None
        
        if collection.default:
            contextMenus = (
                collection.settingsContextMenu(globalC=True),
            )
        else:
            contextMenus = (
                collection.settingsContextMenu(),
                collection.settingsContextMenu(globalC=True)                            
            )
 
        
        
        super(CollectionSourcesLi, self).__init__(title, icon, thumb, url, isFolder, isPlayalbe,
                                       videoInfoLabels, generalInfoLabels, contextMenus)