from src.collection import Collection
from src.li.ItemList import ItemList
from visual.browse_folder import foldersVisual, collectionsVisual, viewStyle




def browse(folder):
    items = ItemList()    
    files, subfolders = folder.listFolder()
    
    
    for subfolder in subfolders:
        if subfolder.name != "_images":
            items.addFolder(subfolder, foldersVisual)
            

    for collectionFile in files:
        collection = Collection.fromFile(collectionFile, loadSources=False)
        items.addCollection(collection, collectionsVisual, deleteContext=True)
        
        
        
    items.present(viewStyle)