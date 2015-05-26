from src.li.types.VideoVisual import VideoVisual
from src.li.types.CollectionVisual import CollectionVisual
from src.li.types.SourceListVisual import SourceListVisual
from src.li.visual.TextSettings import TextSettings
from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.ImageSettings import ImageSettings
from src.youtube.Thumb import ThumbRes


viewStyle          =       ViewStyle.EPISODES



videosVisual = VideoVisual(  
      True,                 #show source? 
      
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
                 


playAllVisual = CollectionVisual(
      TextSettings(
          None,        #color
          False,       #bold?
          False        #italic?
          ),     
                                   
        'special://home/addons/plugin.video.collections/resources/media/play.png',  #default icon
        'special://home/addons/plugin.video.collections/resources/media/play.png',  #default thumb        
        True,                                                                       #force defaults?
        
        customTitle = 'PLAY ALL'
)


browseSourcesVisual = SourceListVisual(  
      'Browse Sources',    #title
      
      TextSettings (        
          None,             #color
          False,            #bold?
          False             #italic?
          ),
                                      
          None,             #icon
          None              #thumb 
)   