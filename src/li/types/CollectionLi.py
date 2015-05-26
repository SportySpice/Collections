from src.li.Li import Li
from src import router
import src.cxml.loader as cxmlLoader

class CollectionLi(Li):
    def __init__(self, collectionFile, collectionVisual, shouldPlay=False):
        xmlRoot = cxmlLoader.root(collectionFile)
        title = collectionVisual.title(xmlRoot)
        
        icon, thumb = collectionVisual.images(collectionFile)
        
        
        playAllUrl = router.playCollectionUrl(collectionFile) 
        
        if shouldPlay:
            url = playAllUrl
            isFolder = False
            isPlayalbe = False      #still false even in this case as we call
                                    #xbmc.player() directly with a play list
            
        else:
            url = router.browseCollectionUrl(collectionFile) 
            isFolder = True
            isPlayalbe = False
            
        generalInfoLabels = None
        videoInfoLabels = None
 
    
        super(CollectionLi, self).__init__(title, icon, thumb, url, isFolder, isPlayalbe,
                                       videoInfoLabels, generalInfoLabels)
        
        
        if not shouldPlay:
            #self.li.addContextMenuItems([("Play All", 'PlayMedia(%s)' % playAllUrl)])
            self.li.addContextMenuItems([("Play All", 'RunPlugin(%s)' % playAllUrl)])