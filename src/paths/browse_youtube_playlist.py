from visual.browse_youtube_playlist import viewStyle, addToCollectionVisual, videosVisual, nextPageVisual
from src.li.ItemList import ItemList
from src.videosource.youtube import Playlist

def browse(playlistFile, pageNum):
    playlist = Playlist.fromCacheFile(playlistFile)

    items = ItemList()
    videos = playlist.videos
    
    if pageNum == 1:
        items.addAddToCollection(playlist, addToCollectionVisual)
    
    for video in videos.updatedPageItems(pageNum):
        items.addVideoPlay(video, videosVisual)
        
        
    if videos.hasPage(pageNum+1):
        items.addYoutubePlaylist(playlist, nextPageVisual, pageNum+1)
    
    items.present(viewStyle)