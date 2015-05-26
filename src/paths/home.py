from visual.home import defaultCollectionsVisual, myCollectionsVisual, VIEW_STYLE
from src.li.ItemList import ItemList

def home(defaultFolder, myFolder):
    items = ItemList()
    items.addFolder(defaultFolder, defaultCollectionsVisual)
    items.addFolder(myFolder, myCollectionsVisual) 

    items.present(VIEW_STYLE)