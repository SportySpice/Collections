from visual.search_youtube_select import viewStyle, channelsVisual, playlistsVisual, bothVisual 
from src.li.ItemList import ItemList
from src import router
from src.videosource.youtube.Search import SearchType

def select():
    items = ItemList()
    
    items.addCustomFolder(router.searchYoutubedUrl(SearchType.CHANNEL), channelsVisual)
    items.addCustomFolder(router.searchYoutubedUrl(SearchType.PLAYLIST), playlistsVisual)
    items.addCustomFolder(router.searchYoutubedUrl(SearchType.BOTH), bothVisual)
    
    items.present(viewStyle)