import sort_videolist as svl
from src.videosource.VideoList import VideoSort as vsr, vsToCounts
from visual.browse_youtube_playlist import viewStyle, addToCollectionVisual, videosVisual, nextPageVisual
from src.li.ItemList import ItemList
from src.videosource.youtube import Playlist
from src.tools.addonSettings import string as st

def browse(playlistFile, pageNum):
    playlist = Playlist.fromCacheFile(playlistFile)

    items = ItemList(hasQeuingVideos=True)
    
    
    if pageNum == 1:
        items.addAddToCollection(playlist, addToCollectionVisual)
        
        
    items.addVideoSortYoutube(st(781))
    
    videos = playlist.videos
    videoList = videos.updatedPageItems(pageNum)
    
    currentSort = svl.loadCurrentSort()
    selected = currentSort.selected
    
    if selected:
        videoList.sort(selected, reverseOrder=currentSort.selectedReverse)   #might cause problems in future cause
        currentSort.setSelectedAsCurrent()                                               #didn't make a copy
        customVcts = vsToCounts[selected]
        videosVisual.setCustomVcts(customVcts)                
    else:           
        currentSort.setCurrent(vsr.DATE, 0, False)    
    
    
    for video in videos.updatedPageItems(pageNum):
        items.addVideo(video, videosVisual)
        
        
    if videos.hasPage(pageNum+1):
        items.addYoutubePlaylist(playlist, nextPageVisual, pageNum+1)
    
    items.present(viewStyle)