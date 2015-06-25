from visual.add_to_collection import BROWSE_DIALOG_HEADING, alreadyInCollectionDialog, successDialog
from src.tools import dialog
from src.tools.dialog import BrowseType
from src import router
from src.file import File
from src.collection import Collection
from src.videosource.VideoSource import SourceType
from src.videosource.youtube import Channel
from src.videosource.youtube import Playlist
from src.videosource.kodi import KodiFolder
from add_to_collection_browse import NEW_COLLECTION_STR, NEW_FOLDER_STR, USE_LAST_FOLDER_STR
from src.paths.root import MY_COLLECTIONS_DIR




def add(vSourceId, vSourceFile, sourceType, relStartPath=''):    
#     import add_to_collection_browse2
#     from src.file import Folder
#     
#     myCollectionFolder = Folder.fromFullpath(MY_COLLECTIONS_DIR)
#     add_to_collection_browse2.browse(myCollectionFolder)
#     return
    
    
        
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
    
    
    if sourceType == SourceType.CHANNEL:        vSource                     = Channel.fromCacheFile(vSourceFile)        
    elif sourceType == SourceType.PLAYLIST:     vSource, needsInfoUpdate    = Playlist.fromPlaylistId(vSourceId)
    else:                                       vSource                     = KodiFolder.fromPath(vSourceId)
        
    
    collection.addCollectionSource(vSource)
    collection.writeCollectionFile()
    
    successDialog(vSource, collection)