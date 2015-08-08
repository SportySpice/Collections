from src.li.ItemList import ItemList
from src.li.types.YoutubePlaylistVisual import YoutubePlaylistVisual
from src.li.visual import TextSettings
from src.li.visual.ViewStyle import ViewStyle
from src.videosource.youtube import Channel

playlistsVisual = YoutubePlaylistVisual(TextSettings.regular())

def browse():
    myChannel = Channel.mine()
    
    items = ItemList()    
    items.addYoutubePlaylist(   myChannel.likesPL,         playlistsVisual)
    items.addYoutubePlaylist(   myChannel.favoritesPL,     playlistsVisual)
    items.addYoutubePlaylist(   myChannel.watchHistoryPL,  playlistsVisual)
    items.addYoutubePlaylist(   myChannel.watchLaterPL,    playlistsVisual)
    
    

    items.present(ViewStyle.FILES)