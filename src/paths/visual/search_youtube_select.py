from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.TextSettings import TextSettings
from src.li.types.CustomFolderVisual import CustomFolderVisual
from src.tools.addonSettings import string as st



viewStyle          =       ViewStyle.TVSHOWS


channelsVisual = CustomFolderVisual (
        st(790),         #title
        
        TextSettings(     
        None,               #color
        False,              #bold?
        False               #italic?
        ),                        
                             
        None,               #icon
        None,               #thumb                                             
)



playlistsVisual = CustomFolderVisual (
        st(791),         #title
        
        TextSettings(     
        None,               #color
        False,              #bold?
        False               #italic?
        ),                        
                             
        None,               #icon
        None,               #thumb                                             
)



bothVisual = CustomFolderVisual (
        st(792),             #title
        
        TextSettings(     
        None,               #color
        False,              #bold?
        False               #italic?
        ),                        
                             
        None,               #icon
        None,               #thumb                                             
)