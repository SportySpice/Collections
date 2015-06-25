from src.li.Li import Li
from src import router

class CollectionSourceLi(Li):
    def __init__(self, cSource):
        title, icon, thumb = cSource.liVisuals()
        thumb = None

        url = cSource.onClickUrl()



        isFolder = True
        isPlayable = False

        generalInfoLabels = None
        videoInfoLabels = None

        
        collection = cSource.collection
        
        if collection.default:
            contextMenus = (collection.settingsContextMenu(globalC=True),)
        
        
        else:
            contextMenus = (
                collection.settingsContextMenu(),
                collection.settingsContextMenu(globalC=True),
                cSource.removeContextMenu()
            )


        super(CollectionSourceLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels, contextMenus)