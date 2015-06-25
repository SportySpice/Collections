from visual.browse_collection_sources import feedVisual
from src.li.ItemList import ItemList
from src.collection import Collection
from src.collection.Collection import OnCollectionClick as occ



def browse(collectionFile):
    collection = Collection.fromFile(collectionFile)
    items = ItemList()
    
    if collection.onClick() == occ.SOURCES:
        items.addCollection(collection, feedVisual, occ.FEED)
        
    for cSource in collection.cSources:
        items.addCollectionSource(cSource)
        
    items.present(collection.sourcesSettings.viewStyle())