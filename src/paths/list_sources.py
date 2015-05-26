from src.li.ItemList import ItemList
from src.collection import loader
from visual.list_sources import sourcesVisual, viewStyle




def listSources(collectionFile):
    collection = loader.load(collectionFile)
    items = ItemList()
        
    for source in collection.sources:
        items.addSource(source, collectionFile, sourcesVisual)
        
    items.present(viewStyle)