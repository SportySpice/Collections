from visual.add_to_collection import noVideosDialog, customTitleDialog, BROWSE_DIALOG_HEADING, alreadyInCollectionDialog, successDialog
from src.tools import dialog
from src.tools.dialog import BrowseType
from src import router
from src.file import File
from src.collection import Collection
from src.videosource.VideoSource import SourceType
from src.videosource.youtube import Channel
from src.videosource.youtube import Playlist
from src.videosource.kodi import KodiFolder
from src.videosource.kodi.FolderVideo import ParseMethod
from add_to_collection_browse import NEW_COLLECTION_STR, NEW_FOLDER_STR, USE_LAST_FOLDER_STR
from src.paths.root import MY_COLLECTIONS_DIR




def add(vSourceId, vSourceFile, sourceType, relStartPath=''):    
#     import add_to_collection_browse2
#     from src.file import Folder
#     
#     myCollectionFolder = Folder.fromFullpath(MY_COLLECTIONS_DIR)
#     add_to_collection_browse2.browse(myCollectionFolder)
#     return

    

    if sourceType == SourceType.FOLDER:
        parseMethod = ParseMethod.NORMAL
        useInFeed = True  
              
        kodiFolder = KodiFolder.fromPath(vSourceId)
        if not kodiFolder.videos():
            result = noVideosDialog(kodiFolder)
            if result == -1:
                return
            
            if result == 0:
                useInFeed = False
    
            if result == 1:
                parseMethod = ParseMethod.FIRST_IN_FOLDER
                
        
        kfTitle = customTitleDialog(kodiFolder).strip()
        if not kfTitle:
            return
        
        vSource = kodiFolder
            
        
    path = router.addToCollectionBrowseUrl(relStartPath + '/')
    
    
    
    
    selection = dialog.browse(BrowseType.SHOW_AND_GET_FILE, BROWSE_DIALOG_HEADING, 'files', useThumbs=True, default=path)
    
    if selection == path:      #this means the user clicked cancel, for whatever reason (xbmc shit...)     
        return
    
    
    if selection.startswith(NEW_COLLECTION_STR):
        import create_new_collection
        
        relativePath = selection[len(NEW_COLLECTION_STR):]
        path = MY_COLLECTIONS_DIR + relativePath
        create_new_collection.create(path, showSuccessDialog=False)
        add(vSourceId, vSourceFile, sourceType, USE_LAST_FOLDER_STR)
        return
    
    if selection.startswith(NEW_FOLDER_STR):
        import create_new_folder
        
        relativePath = selection[len(NEW_FOLDER_STR):]
        path = MY_COLLECTIONS_DIR + relativePath
        create_new_folder.create(path, showSuccessDialog=False)
        add(vSourceId, vSourceFile, sourceType, USE_LAST_FOLDER_STR)
        return
    
    
    
    
    collectionFile = File.fromFullpath(selection)
    collection = Collection.fromFile(collectionFile)
    
    if collection.hasSource(vSourceId):
        cSource = collection.getCSource(vSourceId)        
        alreadyInCollectionDialog(cSource.videoSource, collection)
        return
    
    
    if sourceType == SourceType.FOLDER:
        cSource = collection.addCollectionSource(kodiFolder, useInFeed=useInFeed, kodiParseMethod=parseMethod, customTitle=kfTitle)
    
    else:
        if sourceType == SourceType.CHANNEL:    vSource                     = Channel.fromCacheFile(vSourceFile)        
        else:                                   vSource, needsInfoUpdate    = Playlist.fromPlaylistId(vSourceId)
        
        cSource = collection.addCollectionSource(vSource)
        

    collection.writeCollectionFile()
    
    successDialog(cSource, collection)