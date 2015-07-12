from visual.remove_from_collection import confirmDialog, successDialog
from src.collection import Collection
from src.tools import xbmcTool


def remove(collectionFile, sourceId, showConfirmDialog=True, showSuccessDialog=True, refreshContainer=True):
    collection = Collection.fromFile(collectionFile)
    cSource = collection.getCSource(sourceId)
    
    removeDirect(cSource, showConfirmDialog, showSuccessDialog, refreshContainer)
    
    
    
def removeDirect(cSource, showConfirmDialog=True, showSuccessDialog=True, refreshContainer=True):
    collection = cSource.collection
    
    if showConfirmDialog:
        if not confirmDialog(cSource, collection): 
            return False
        
        
    collection.removeCSource(cSource.id)
    collection.writeCollectionFile()
    
    if showSuccessDialog:
        successDialog(cSource, collection)
        
    
    if refreshContainer:
        xbmcTool.refreshContainer()
        
    return True