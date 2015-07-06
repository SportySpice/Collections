from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.TextSettings import TextSettings
from src.li.types.AddToCollectionVisual import AddToCollectionVisual
from src.li.types.KodiFolderVisual import KodiFolderVisual
#from src.li.types.KodiVideoVisual import KodiVideoVisual
from src.li.types.VideoVisual import VideoVisual
from src.li.visual.FullTextSettings import FullTextSettings, Location
from src.tools.addonSettings import string as st


viewStyle           =       ViewStyle.EPISODES





addToCollectionVisual = AddToCollectionVisual (
        st(750),        #title

        TextSettings(
        None,           #color
        False,          #bold?
        False           #italic?
        ),
                                               
        None,           #icon
        None,           #thumb
)


foldersVisual = KodiFolderVisual(
      TextSettings(
          None,        #color
          False,       #bold?
          False        #italic?
          ),                                      
)



# videosVisual = KodiVideoVisual(
#       TextSettings(
#           None,        #color
#           False,       #bold?
#           False        #italic?
#           ),                                      
# )

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
                     
#         count2TS=TextSettings(
#             'yellow',           #color
#             False,              #bold?           
#             False,              #italic?
#         ),
        
        countLocation = Location.LEFT_ALIGNED
    )                                 
)