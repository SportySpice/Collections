import sort_videolist as svl
from visual.browse_youtube_channel import viewStyle, addToCollectionVisual, playlistsVisual, videosVisual, nextPageVisual
from src.li.ItemList import ItemList
from src.videosource.youtube import Channel
from src.videosource.VideoSource import SourceType
from src.videosource.VideoList import VideoSort as vsr, vsToCounts
from src.tools.addonSettings import string as st


VIDEO_SORT_OPTIONS  = (vsr.DATE, vsr.VIEWS,  vsr.DURATION,  vsr.SHUFFLE,    vsr.VIDEO_TITLE,    vsr.RATING, vsr.LIKES,  vsr.DISLIKES,   vsr.COMMENTS,   vsr.PLAYCOUNT,  vsr.LASTPLAYED)
VIDEO_SORT_LABELS   = (st(620),  st(621),    st(622),       st(624),        st(627),            st(628),    st(629),    st(630),        st(631),        st(632),        st(633)       )


def browse(channelFile, pageNum):
    channel = Channel.fromCacheFile(channelFile)
    
    if channel.needsInfoUpdate(checkUploadPlaylist=True):
        channel.fetchInfo()
    
    
    items = ItemList(hasQeuingVideos=True)    
    
    if pageNum == 1:
        items.addAddToCollection(channel, addToCollectionVisual)
        items.addYoutubeChannelPlaylists(channel, playlistsVisual)
        
    items.addVideoSortYoutube(st(772))
    
    videos = channel.videos
    videoList = videos.updatedPageItems(pageNum)
    
    currentSort = svl.loadCurrentSort(SourceType.CHANNEL)
    selected = currentSort.selected
    
    if selected:
        videoList.sort(selected, reverseOrder=currentSort.selectedReverse)   #might cause problems in future cause
        currentSort.setSelectedAsCurrent()                                               #didn't make a copy
        customVcts = vsToCounts[selected]
        videosVisual.setCustomVcts(customVcts)                
    else:           
        currentSort.setCurrent(vsr.DATE, 0, False)
        
    
    
    for video in videoList:
        items.addVideo(video, videosVisual)
        
    
    if videos.hasPage(pageNum+1):
        items.addYoutubeChannel(channel, nextPageVisual, pageNum+1)
        
    items.present(viewStyle)