from src.li.Li import Li
from src import router
from src.collection.Collection import OnCollectionClick as occ

class CollectionLi(Li):
    def __init__(self, collection, collectionVisual, onClick=None, deleteContext=False):
        title = collectionVisual.title(collection)
        
        icon, thumb = collectionVisual.images(collection)
        
        
        isPlayable = False
        playAllUrl = router.playCollectionUrl(collection.file)
        
        
        if onClick is None:                        
            onClick = collection.onClick()
                    
        
        
        isFolder = True    
                                 
        if  onClick == occ.FEED:            url = router.browseCollectionUrl(collection.file)
        elif onClick == occ.SOURCES:        url = router.browseCollectionSourcesUrl(collection.file)
        elif onClick == occ.SOURCES_ONLY:   url = router.browseCollectionSourcesUrl(collection.file)
        elif onClick == occ.PLAYALL:
            url = playAllUrl
            isFolder = False
        else:
            raise ValueError('Unexpected onClick Value!')
        

        
        if collection.default:
            contextMenus = [
                collection.playAllContextMenu(),
                collection.settingsContextMenu(globalC=True)
            ] 
        
        else:
            contextMenus = [
                collection.playAllContextMenu(),
                collection.settingsContextMenu(),
                collection.settingsContextMenu(globalC=True),                
            ]
            
            if deleteContext:
                contextMenus.append(collection.deleteContextMenu())
            
        generalInfoLabels = None
        videoInfoLabels = None
 
    
        super(CollectionLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels, contextMenus)