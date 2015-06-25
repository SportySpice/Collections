from src.li.visual.ViewStyle import ViewStyle
from src.li.types.VideoVisual import VideoVisual
from src.li.types.AddToCollectionVisual import AddToCollectionVisual
from src.li.types.YoutubeChannelVisual import YoutubeChannelVisual
from src.li.types.YoutubeChannelPlaylistsVisual import YoutubeChannelPlaylistsVisual
from src.li.visual.FullTextSettings import FullTextSettings
from src.li.visual.TextSettings import TextSettings
from src.li.visual.CountTextSettings import CountTextSettings, Location, CountType
from src.tools.addonSettings import string as st



viewStyle          =       ViewStyle.EPISODES



addToCollectionVisual = AddToCollectionVisual (
        st(770),   #title

        TextSettings(
        None,           #color
        False,          #bold?
        False           #italic?
        ),
                                               
        None,           #icon
        None,           #thumb
)





playlistsVisual = YoutubeChannelPlaylistsVisual (
        st(771),        #title
        False,          #title has page number?
        
        TextSettings(
        None,           #color
        False,          #bold?
        False           #italic?
        ),   
)



videosVisual = VideoVisual (
    FullTextSettings(
        TextSettings(   #title
            'None',       #color
            False,      #bold?
            False,      #italic?
        ),
        
        sourceTS=TextSettings (
            'red',      #color
            False,      #bold?
            False,      #italic?
            False       #show?
        ),
        
        countTS=CountTextSettings(
            'yellow',           #color
            False,              #bold?           
            False,              #italic?
            Location.LEFT,      #location 
            CountType.VIDEOS, 
            True)               #show?
    )                                             
)



nextPageVisual = YoutubeChannelVisual (
        TextSettings(
        None,           #color
        False,          #bold?
        False           #italic?
        ),   
                                               
        customTitle = st(980),
        ctHasPageNum = True,
        noThumb = True              
)