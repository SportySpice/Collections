from src.file import File, Folder
from src.tools import addonSettings


DEFAULT_COLLECTIONS_DIR =       'special://home/addons/plugin.video.collections/resources/default_collections'
MY_COLLECTIONS_DIR      =       'special://profile/addon_data/plugin.video.collections/collections'

DATA_DIR                =       'special://profile/addon_data/plugin.video.collections/data'
GENERAL_DATA_DIR        =       'special://profile/addon_data/plugin.video.collections/data/general'
VIEWS_DATA_DIR          =       'special://profile/addon_data/plugin.video.collections/data/views'
KODI_DATA_DIR           =       'special://profile/addon_data/plugin.video.collections/data/kodi'
KODI_ESTIMATION_DIR     =       'special://profile/addon_data/plugin.video.collections/data/kodi/estimation'
YOUTUBE_DATA_DIR        =       'special://profile/addon_data/plugin.video.collections/data/youtube'



CACHE_DIR               =       'special://profile/addon_data/plugin.video.collections/cache'
GENERAL_CACHE_DIR       =       'special://profile/addon_data/plugin.video.collections/cache/general'
KODI_FOLDER_CACHE_DIR   =       'special://profile/addon_data/plugin.video.collections/cache/kodi/folders'
YOUTUBE_CACHE_DIR       =       'special://profile/addon_data/plugin.video.collections/cache/youtube'
CHANNEL_CACHE_DIR       =       'special://profile/addon_data/plugin.video.collections/cache/youtube/channels'
PLAYLIST_CACHE_DIR      =       'special://profile/addon_data/plugin.video.collections/cache/youtube/playlists'
CATEGORY_CACHE_DIR      =       'special://profile/addon_data/plugin.video.collections/cache/youtube/categories'
SEARCH_CACHE_DIR        =       'special://profile/addon_data/plugin.video.collections/cache/youtube/searches'

CURRENT_VERSION_FILE    =       'current_ver'


def root():
    createDataFolders()
    checkVersionChange()
    createCacheFolders()
    
    
    defaultCollectionsFolder    =   Folder.fromFullpath(DEFAULT_COLLECTIONS_DIR)
    myCollectionsFolder         =   Folder.fromFullpath(MY_COLLECTIONS_DIR)
    myCollectionsFolder.createIfNotExists()
    
    #homeSetting = addonSettings.get('homepage', default=0,  isInt=True)    
    
    homeSetting = addonSettings.get('homepage', default='0')  #temp thing cause of people changing version. remove later                      
    if not homeSetting.isdigit():          
        addonSettings.set('homepage', '0')
        homeSetting = 0
    else:
        homeSetting = int(homeSetting)
    
    
    options = {0:_home, 1:_defaultCollections, 2:_myCollections}
    
    
    
    options[homeSetting](defaultCollectionsFolder, myCollectionsFolder)



def checkVersionChange():
    addonVer = addonSettings.version()
    currentVerFile = File.fromNameAndDir(CURRENT_VERSION_FILE, GENERAL_DATA_DIR)
    
    if currentVerFile.exists() and (currentVerFile.loadObject() == addonVer):
        return
    
    import delete_cache
    delete_cache.delete(successDialog=False)
    currentVerFile.dumpObject(addonVer)
    
    
    
        
    
    
    
    
    
def createCacheFolders():
    cacheFolders = (
        Folder.fromFullpath(CACHE_DIR),
        Folder.fromFullpath(GENERAL_CACHE_DIR),
        Folder.fromFullpath(KODI_FOLDER_CACHE_DIR),
        Folder.fromFullpath(CHANNEL_CACHE_DIR),
        Folder.fromFullpath(PLAYLIST_CACHE_DIR),
        Folder.fromFullpath(CATEGORY_CACHE_DIR),
        Folder.fromFullpath(SEARCH_CACHE_DIR)
    )
    
    for folder in cacheFolders:
        folder.createIfNotExists()


def createDataFolders():
    dataFolders = (
        Folder.fromFullpath(DATA_DIR),
        Folder.fromFullpath(VIEWS_DATA_DIR),
        Folder.fromFullpath(GENERAL_DATA_DIR),
        Folder.fromFullpath(KODI_DATA_DIR),
        Folder.fromFullpath(KODI_ESTIMATION_DIR),
        Folder.fromFullpath(YOUTUBE_DATA_DIR),
    )

    for folder in dataFolders:
        folder.createIfNotExists()
   
    
    
    
def _home(defaultFolder, myFolder):
    import home
    home.home(defaultFolder, myFolder)
    

    
    
def _defaultCollections(defaultFolder, myFolder):
    import browse_folder
    browse_folder.browse(defaultFolder)
    
    
    
    
def _myCollections(defaultFolder, myFolder):
    import browse_folder
    browse_folder.browse(myFolder)