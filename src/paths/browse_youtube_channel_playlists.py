from src.li.ItemList import ItemList
from visual.browse_youtube_channel_playlists import viewStyle, playlistsVisual, nextPageVisual
from src.videosource.youtube import Channel

def browse(channelFile, pageNum):
    channel = Channel.fromCacheFile(channelFile)
    
    items = ItemList()
    playlists = channel.playlists
    
    for playlist in playlists.updatedPageItems(pageNum):
        items.addYoutubePlaylist(playlist, playlistsVisual)
        
    
    if playlists.hasPage(pageNum+1):
        items.addYoutubeChannelPlaylists(channel, nextPageVisual, pageNum+1)
        
    items.present(viewStyle)