from src.li.visual.ViewStyle import ViewStyle
from src.li.types.VideoVisual import VideoVisual
from src.li.types.AddToCollectionVisual import AddToCollectionVisual
from src.li.types.YoutubePlaylistVisual import YoutubePlaylistVisual
from src.li.visual.FullTextSettings import FullTextSettings, Location
from src.li.visual.TextSettings import TextSettings
from src.tools.addonSettings import string as st


viewStyle          =       ViewStyle.EPISODES


addToCollectionVisual = AddToCollectionVisual (
        st(780),   #title

        TextSettings(
        None,           #color
        False,          #bold?
        False           #italic?
        ),
                                               
        None,           #icon
        None,           #thumb
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
        
        countTS=TextSettings(
            'steelblue',        #color
            False,              #bold?           
            False,              #italic?
        ),
                     
        count2TS=TextSettings(
            'yellow',           #color
            False,              #bold?           
            False,              #italic?
        ),
        
        countLocation = Location.LEFT_ALIGNED
    )                                 
)



nextPageVisual = YoutubePlaylistVisual (
        TextSettings(
        None,           #color
        False,          #bold?
        False           #italic?
        ),      
                                        
        customTitle = st(980),
        ctHasPageNum = True        
)