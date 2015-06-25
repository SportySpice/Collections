from visual.remove_from_collection import confirmDialog, successDialog
from src.collection import Collection
import xbmc


def remove(collectionFile, sourceId, showConfirmDialog=True, showSuccessDialog=True, refreshContainer=True):
    collection = Collection.fromFile(collectionFile)
    cSource = collection.getCSource(sourceId)
    
    removeDirect(cSource, showConfirmDialog, showSuccessDialog, refreshContainer)
    
    
    
def removeDirect(cSource, showConfirmDialog=True, showSuccessDialog=True, refreshContainer=True):
    collection = cSource.collection
    vSource = cSource.videoSource
    
    if showConfirmDialog:
        if not confirmDialog(vSource, collection): 
            return False
        
        
    collection.removeCSource(cSource.id)
    collection.writeCollectionFile()
    
    if showSuccessDialog:
        successDialog(vSource, collection)
        
    
    if refreshContainer:
        xbmc.executebuiltin('XBMC.Container.Refresh()')
        
    return True