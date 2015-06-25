from visual.browse_youtube_channel import viewStyle, addToCollectionVisual, playlistsVisual, videosVisual, nextPageVisual
from src.li.ItemList import ItemList
from src.videosource.youtube import Channel

def browse(channelFile, pageNum):
    channel = Channel.fromCacheFile(channelFile)
    
    if channel.needsInfoUpdate(checkUploadPlaylist=True):
        channel.fetchInfo()
    
    
    items = ItemList()
    videos = channel.videos
    
    
    
    if pageNum == 1:
        items.addAddToCollection(channel, addToCollectionVisual)
        items.addYoutubeChannelPlaylists(channel, playlistsVisual)
    
    for video in videos.updatedPageItems(pageNum):
        items.addVideoPlay(video, videosVisual)
        
    
    if videos.hasPage(pageNum+1):
        items.addYoutubeChannel(channel, nextPageVisual, pageNum+1)
        
    items.present(viewStyle)