import sort_videolist as svl
from src.collection import Collection
from src.collection.Collection import OnCollectionClick as occ
from src.videosource.VideoList import vsToCounts
from src.li.ItemList import ItemList






def present(collectionFile):
    collection = Collection.fromFile(collectionFile)
    
        
    currentSort = svl.loadCurrentSort()
    selected = currentSort.selected
    
    if selected:
        collection.createCombinedList(customSort=selected, reverse=currentSort.selectedReverse)
        currentSort.setSelectedAsCurrent()
        customVcts = vsToCounts[selected]
    else:
        collection.updateDatedSources()
              
        vs = collection.feedSettings.sort()
        index = vs - 1  #very scatchy use of this enum, change later if causes problems
        reverse = collection.feedSettings.reverseSort()
        
        currentSort.setCurrent(vs, index, reverse)
        customVcts = None
    
    
    fs = collection.feedSettings
    ts = fs.TS
    
    items = ItemList(not fs.playVideoOnly())
    
    
    if collection.onClick() == occ.FEED:
        items.addCollectionSources(collection)
    
    if fs.showSettings() and not (collection.default):
        items.addCollectionSettings(collection)
        
    if fs.showSort():
        items.addVideoSortCollection(collection)
    
    if fs.showPlayAll():    
        items.addCollection(collection, ts.playAllVisual(), onClick=occ.PLAYALL)
        

    
    
    videosVisual = ts.videosVisual(customVcts)
    for video in collection.videos:
        items.addVideo(video, videosVisual, collection)            
    
    
    items.present(collection.feedSettings.viewStyle())