from visual.home import defaultCollectionsVisual, myCollectionsVisual, browseForSourcesVisual, VIEW_STYLE
from src.li.ItemList import ItemList
from src import router

def home(defaultFolder, myFolder):
    items = ItemList()
    
    items.addFolder(defaultFolder, defaultCollectionsVisual)
    items.addFolder(myFolder, myCollectionsVisual)
    items.addCustomFolder(router.browseForSourcesUrl(), browseForSourcesVisual)

    items.present(VIEW_STYLE)