from src import router
from src.li.Li import Li
#from src.tools.addonSettings import string as st

class CollectionSettingsLi(Li):
    def __init__(self, collection=None):
        if collection:
            title, icon, thumb = collection.feedSettings.TS.settingsVisuals()
            url = router.editCollectionUrl(collection.file)
            contextMenus = (
                collection.settingsContextMenu(),
                collection.settingsContextMenu(globalC=True)
            )
            
#         else:   #this is never actually used.
#             title = st(30403)        
#             icon = None
#             thumb = None
#             url = router.editCollectionUrl()
#             contextMenus = None
        
        
            
        
        isFolder = False
        isPlayable = False
            
        generalInfoLabels = None
        videoInfoLabels = None
 
    
        super(CollectionSettingsLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels, contextMenus)