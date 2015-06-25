from src.collection import Collection
from src.collection.Collection import OnCollectionClick as occ
from src.li.ItemList import ItemList



def present(collectionFile):
    collection = Collection.fromFile(collectionFile)
    collection.updateDatedSources()          
    
    
    
    items = ItemList()
    fs = collection.feedSettings
    ts = fs.TS
    
    if collection.onClick() == occ.FEED:
        items.addCollectionSources(collection)
    
    if fs.showSettings() and not (collection.default):
        items.addCollectionSettings(collection)
    
    if fs.showPlayAll():    
        items.addCollection(collection, ts.playAllVisual(), onClick=occ.PLAYALL)
        

    
    
    if fs.playVideoOnly():
        for video in collection.videos:            
            items.addVideoPlay(video, ts.videosVisual(), collection)
        
    else:      
        for video in collection.videos:            
            items.addVideoQueueCollection(video, collection, ts.videosVisual())                
    
    
    items.present(collection.feedSettings.viewStyle())