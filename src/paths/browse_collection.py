from src.collection import loader
from src.li.ItemList import ItemList
from visual.browse_collection import playAllVisual, videosVisual, browseSourcesVisual, viewStyle
import xbmcaddon


def present(collectionFile):
    collection = loader.load(collectionFile)
    collection.updateVideosIfTime()       
          
    items = ItemList()
    
    items.addCollection(collection.file, playAllVisual, shouldPlay=True)
    items.addSourceList(collectionFile, browseSourcesVisual)
    
    
    if xbmcaddon.Addon().getSetting('video_behaviour') == 'Play Video Only':
        for video in collection.videoList:            
            items.addVideo(video, videosVisual)
        
    else:       #will happen even if nothing is set, aka it's the defualt
        for video in collection.videoList:            
            items.addVideo(video, videosVisual, special=True, collectionFile=collectionFile)                
    
    
    items.present(viewStyle)