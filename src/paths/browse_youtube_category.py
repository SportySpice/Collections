from visual.browse_youtube_category import viewStyle, channelsVisual, nextPageVisual
from src.li.ItemList import ItemList
from src.videosource.youtube import Category



def browse(categoryFile, pageNum):
    category = Category.fromCacheFile(categoryFile)
    
    
    items = ItemList()
    channels = category.channels
    
    for channel in channels.updatedPageItems(pageNum):
        items.addYoutubeChannel(channel, channelsVisual)
        
        
    if channels.hasPage(pageNum+1):
        items.addYoutubeCategory(category, nextPageVisual, pageNum+1)
        
    items.present(viewStyle)