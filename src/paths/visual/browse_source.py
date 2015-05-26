from src.li.types.VideoVisual import VideoVisual
from src.li.visual.TextSettings import TextSettings
from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.ImageSettings import ImageSettings
from src.youtube.Thumb import ThumbRes


viewStyle          =       ViewStyle.EPISODES



videosVisual = VideoVisual(  
      False,                 #show source? 
      
      TextSettings (        #source text settings
          'red',            #color
          False,            #bold?
          False             #italic?
          ),
      
      TextSettings (        #title text settings
          None,             #color
          False,            #bold?
          False             #italic?
        ),
                          
        ImageSettings (
            ThumbRes.HIGHEST,     #icon res
            ThumbRes.HIGHEST      #thumb res                       
        )                          
)      