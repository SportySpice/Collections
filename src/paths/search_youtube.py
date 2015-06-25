from visual.search_youtube import viewStyle, keyboardHeading, channelsVisual, playlistsVisual, nextPageVisual
from src.tools import keyboard
from src.li.ItemList import ItemList
from src.videosource.youtube.Search import Search, SearchType, fromCacheFile

from src import router

def search(searchType=None, searchFile=None, pageNum=1):
    if searchFile:
        search = fromCacheFile(searchFile)
        
    else:    
        heading = keyboardHeading[searchType]
        keyboard.show(heading)
    
        if keyboard.gotInput():
            query = keyboard.text()
            search = Search(query, searchType)
        else:
            return
    
        
    
    
    
    if search.searchType != SearchType.BOTH:
        channelsVisual.preTitle = None
        playlistsVisual.preTitle = None
        
    items = ItemList()
    results = search.results
        
    for result in results.updatedPageItems(pageNum):
        if result.isChannel():
            channel = result
            items.addYoutubeChannel(channel, channelsVisual)
            
        else:
            playlist = result
            items.addYoutubePlaylist(playlist, playlistsVisual)
        
    
    
    if results.hasPage(pageNum+1):
        items.addCustomFolder(router.searchYoutubedUrl(searchFile=search.cacheFile, pageNum=pageNum+1), nextPageVisual(pageNum+1))
        
        
    items.present(viewStyle)
