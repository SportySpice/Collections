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
        gc.setLoadedSources()
        
        gc.feedSettings.useLimits = True    #temp cause of people changing from version 2.0.1 where
                                            #this attrib didn't exist. remove this in future
    
    else:
        gc = Collection.empty('Global Collection', gcFile)
        
        gc.setOnClick(Collection.D_ONCLICK)
                        
        gc.feedSettings.use = True
        gc.feedSettings.useLimits = True
        gc.feedSettings.TS.use = True
        gc.sourcesSettings.use = True
        gc.sourcesSettings.TS.use = True
        
        gc.writeCollectionFile()
        
    
    _globalCollection = gc
    return gc