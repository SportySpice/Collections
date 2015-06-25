from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.TextSettings import TextSettings
from src.videosource.youtube.Search import SearchType
from src.li.types.YoutubeChannelVisual import YoutubeChannelVisual
from src.li.types.YoutubePlaylistVisual import YoutubePlaylistVisual
from src.li.types.CustomFolderVisual import CustomFolderVisual
from src.tools.addonSettings import string as st

viewStyle          =       ViewStyle.TVSHOWS

keyboardHeading = {
        SearchType.CHANNEL:     st(800),
        SearchType.PLAYLIST:    st(801),
        SearchType.BOTH:        st(802)
}



channelsVisual = YoutubeChannelVisual (                
        TextSettings(           
        None,              #color
        False,             #bold?
        False              #italic?
        ),
                                       
        preTitle = '[CH] ',
        
        preTitleTextSettings = TextSettings(
        'red',             #color
        False,             #bold?
        False              #italic?
        )                                              
)



playlistsVisual = YoutubePlaylistVisual (                
        TextSettings(           
        None,              #color
        False,             #bold?
        False              #italic?
        ),             
                                         
        preTitle = '[PL] ',
        
        preTitleTextSettings = TextSettings(
        'red',             #color
        False,             #bold?
        False              #italic?
        )                                   
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