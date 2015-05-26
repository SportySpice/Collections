from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.TextSettings import TextSettings
from src.li.visual.ImageSettings import ImageSettings
from src.youtube.Thumb import ThumbRes
from src.li.types.SourceVisual import SourceVisual

viewStyle           =       ViewStyle.TVSHOWS


sourcesVisual = SourceVisual(  
      TextSettings (        
          None,            #color
          False,           #bold?
          False            #italic?
          ),
                          
        ImageSettings (
            ThumbRes.HIGHEST,     #icon res
            ThumbRes.HIGHEST      #thumb res                       
        )                          
)      