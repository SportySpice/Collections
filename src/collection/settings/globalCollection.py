from src.paths.root import VIEWS_DATA_DIR
from src.file import File



GLOBAL_COLLECTION_FILE = 'globalCollection.xml'
_globalCollection = None



def gc():    
    global _globalCollection
    
    if _globalCollection:
        return _globalCollection
    
    from src.collection import Collection           
    gcFile = File.fromNameAndDir(GLOBAL_COLLECTION_FILE, VIEWS_DATA_DIR)
        
    if gcFile.exists():        
        gc = Collection.fromFile(gcFile, loadSources=False, isGlobal=True)
    
    else:
        gc = Collection.empty('Global Collection', gcFile)
        
        gc.setOnClick(Collection.D_ONCLICK)
                        
        gc.feedSettings.use = True
        gc.feedSettings.TS.use = True
        gc.sourcesSettings.use = True
        gc.sourcesSettings.TS.use = True
        
        gc.writeCollectionFile()
        
    
    _globalCollection = gc
    return gc