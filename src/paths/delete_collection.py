from visual.delete_collection import confirmDialog, successDialog
from src.collection import Collection
import xbmc


def delete(collectionFile, showConfirmDialog=True, showSuccessDialog=True, refreshContainer=True):
    collection = Collection.fromFile(collectionFile, loadSources=False)
    
    if showConfirmDialog:
        if not confirmDialog(collection): 
            return False
        
    
    collection.file.delete()
    
    
    if showSuccessDialog:
        successDialog(collection)
    
    del collection    
    
    if refreshContainer:
        xbmc.executebuiltin('XBMC.Container.Refresh()')
        
    return True