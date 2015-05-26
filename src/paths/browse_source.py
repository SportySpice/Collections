from src.collection import loader
from src.li.ItemList import ItemList
from visual.browse_source import viewStyle, videosVisual
import xbmcaddon

def browse(sourceId, collectionFile):
    collection = loader.load(collectionFile)    
    source = collection.getSource(sourceId)
    source.updateUnlimitedVideos()
    collection.dump()                   ###temp solution, should happen automatically when
                                        ###when calling updateUnlimitedVideos()
    items = ItemList()
    
    
    if xbmcaddon.Addon().getSetting('video_behaviour') == 'Play Video Only':
        for video in source.unlimitedVideos():            
            items.addVideo(video, videosVisual)
        
    else:       #will happen even if nothing is set, aka it's the defualt
        for video in source.unlimitedVideos():            
            items.addVideo(video, videosVisual, sourceSpecial=True, sourceId=sourceId, collectionFile=collectionFile) 
    
    
    items.present(viewStyle)