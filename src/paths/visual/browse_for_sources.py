from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.TextSettings import TextSettings
from src.li.types.CustomFolderVisual import CustomFolderVisual
from src.li.types.KodiFolderVisual import KodiFolderVisual
from src.tools.addonSettings import string as st


viewStyle           =       ViewStyle.FILES

def customFoldersVisual(title):
    return CustomFolderVisual(
        title,
        TextSettings(
            None,        #color
            False,       #bold?
            False        #italic?
        ),     
                                   
        None,       #icon
        None,       #thumb
    )
    
youtubeSearchVisual         = customFoldersVisual(  st(700) )
youtubeSubscriptionsVisual  = customFoldersVisual(  st(701) )
youtubeCategoriesVisual     = customFoldersVisual(  st(702) )




kodiFoldersVisual = KodiFolderVisual(
    TextSettings(
        None,        #color
        False,       #bold?
        False        #italic?
    ),                            
)



#localStorageVisual          = customFoldersVisual(st(740))