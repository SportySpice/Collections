from src.li.types.YoutubePlaylistVisual import YoutubePlaylistVisual
from src.li.types.YoutubeChannelPlaylistsVisual import YoutubeChannelPlaylistsVisual
from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.TextSettings import TextSettings
from src.tools.addonSettings import string as st


viewStyle          =       ViewStyle.TVSHOWS


playlistsVisual = YoutubePlaylistVisual (                
        TextSettings(           
        None,              #color
        False,             #bold?
        False              #italic?
        ),                                                
)



nextPageVisual = YoutubeChannelPlaylistsVisual ( 
        st(980),    #title
        True,               #title has page number?
        
        TextSettings(           
        None,              #color
        False,             #bold?
        False              #italic?
        ),                                                
) 