from src.li.types.YoutubeChannelVisual import YoutubeChannelVisual
from src.li.types.YoutubeCategoryVisual import YoutubeCategoryVisual
from src.li.visual.TextSettings import TextSettings
from src.li.visual.ViewStyle import ViewStyle
from src.tools.addonSettings import string as st


viewStyle          =       ViewStyle.TVSHOWS



channelsVisual = YoutubeChannelVisual (
        TextSettings(
        None,        #color
        False,       #bold?
        False        #italic?
        ),                        
)


nextPageVisual = YoutubeCategoryVisual (
        TextSettings(
        None,           #color
        False,          #bold?
        False           #italic?
        ),   
                                               
        st(980),        #custom title
        True            #custom title has page number?              
)