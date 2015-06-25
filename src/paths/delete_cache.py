from visual.delete_cache import successDialog as _successDialog
from src.file import Folder
import root
from root import CACHE_DIR





def delete(successDialog=True):
    cacheFolder = Folder.fromFullpath(CACHE_DIR)
    cacheFolder.deleteIfExists()
    
    if successDialog:
        _successDialog()
    
    
    root.createCacheFolders()