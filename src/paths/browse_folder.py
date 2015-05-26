import xbmcaddon
from src.li.ItemList import ItemList
from visual.browse_folder import foldersVisual, collectionsVisual, viewStyle





def explore(folder):
    items = ItemList()    
    files, subfolders = folder.listFolder()
    
    
    for subfolder in subfolders:
        if subfolder.name != "_images":
            items.addFolder(subfolder, foldersVisual)
            
        
      
        
    if xbmcaddon.Addon().getSetting('collection_behaviour') == 'Play All':
        shouldPlay = True
    else:                                                                   #will happen even if nothing is set, aka it's the defualt
        shouldPlay = False

    for collectionFile in files:
        items.addCollection(collectionFile, collectionsVisual, shouldPlay)
        
        
        
    items.present(viewStyle)