from src.file import Folder
import xbmcaddon


DEFAULT_COLLECTIONS_DIR =       'special://home/addons/plugin.video.collections/resources/default_collections'
#USERDATA_DIR            =       'special://profile/addon_data/plugin.video.collections'
MY_COLLECTIONS_DIR      =       'special://profile/addon_data/plugin.video.collections/collections'
CACHE_DIR               =       'special://profile/addon_data/plugin.video.collections/cache'




def root():
    defaultFolder       =   Folder.fromFullpath(DEFAULT_COLLECTIONS_DIR)
    myCollectionsFolder =   Folder.fromFullpath(MY_COLLECTIONS_DIR)
    cacheFolder         =   Folder.fromFullpath(CACHE_DIR)
    
    myCollectionsFolder.createIfNotExists()
    cacheFolder.createIfNotExists() 
    
    
    homeSetting = xbmcaddon.Addon().getSetting('homepage')
    
    options = {'':_home, 'Home':_home, 'Default Collections':_defaultCollections,
              'My Collections':_myCollections}
    
    options[homeSetting](defaultFolder, myCollectionsFolder)
    
    
    
    
    
    
    
    
    
    
    
def _home(defaultFolder, myFolder):
    import home
    home.home(defaultFolder, myFolder)
    

    
    
def _defaultCollections(defaultFolder, myFolder):
    import browse_folder
    browse_folder.explore(defaultFolder)
    
    
    
    
def _myCollections(defaultFolder, myFolder):
    import browse_folder
    browse_folder.explore(myFolder)