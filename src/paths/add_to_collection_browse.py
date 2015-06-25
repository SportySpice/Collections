from src.collection import Collection
from visual.add_to_collection_browse import viewStyle, foldersVisual, createNewCollectionVisual, collectionsVisual, createNewFolderVisual
from src.li.ItemList import ItemList
from src.paths.root import MY_COLLECTIONS_DIR
from src.file import Folder
from src.file import File
from src.paths.root import GENERAL_CACHE_DIR

LAST_FOLDER_FILE = 'add_to_c_last_folder'

NEW_COLLECTION_STR  = 'newCollection'
NEW_FOLDER_STR      = 'newFolder'

USE_LAST_FOLDER_STR = 'useLastFolderRrRr'


def browse(relativePath):
    lastFolderFile = File.fromNameAndDir(LAST_FOLDER_FILE, GENERAL_CACHE_DIR)
    
    
    if relativePath.endswith('/'):
        relativePath = relativePath[:-1]
        
    if relativePath == USE_LAST_FOLDER_STR:
        relativePath = lastFolderFile.loadObject()
    
    path = MY_COLLECTIONS_DIR + relativePath
    folder = Folder.fromFullpath(path) 
    
    items = ItemList()
    
    
    
    files, subfolders = folder.listFolder()
    
    for subfolder in subfolders:
        if subfolder.name != "_images":
            subpath = relativePath + '/' + subfolder.name
            items.addSelectableFolder(subfolder, foldersVisual, subpath)
            
    
    items.addCustomFile(NEW_COLLECTION_STR + relativePath, createNewCollectionVisual)
    items.addCustomFile(NEW_FOLDER_STR + relativePath, createNewFolderVisual)
            
        
    

    for collectionFile in files:
        collection = Collection.fromFile(collectionFile, loadSources=False)
        items.addSelectableCollection(collection, collectionsVisual)
        
    
    
    lastFolderFile.dumpObject(relativePath)
        
    items.present(viewStyle)