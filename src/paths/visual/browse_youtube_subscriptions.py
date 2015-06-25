from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.TextSettings import TextSettings
from src.li.types.YoutubeChannelVisual import YoutubeChannelVisual
from src.li.types.CustomFolderVisual import CustomFolderVisual
from src.tools.addonSettings import string as st



viewStyle          =       ViewStyle.TVSHOWS


channelsVisual = YoutubeChannelVisual (                             
        TextSettings(            
        None,               #color
        False,              #bold?
        False               #italic?
        ),                                                
)


def nextPageVisual(pageNum):
    return CustomFolderVisual (
            st(980) %pageNum,        #title
                                     
            TextSettings(            
            None,               #color
            False,              #bold?
            False               #italic?
            ),
                                         
            None,               #icon
            None                #thumb                           
    )




