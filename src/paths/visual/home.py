from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.TextSettings import TextSettings
from src.li.types.FolderVisual import FolderVisual


VIEW_STYLE           =       ViewStyle.TVSHOWS


defaultCollectionsVisual = FolderVisual(
      TextSettings(
          None,        #color
          False,       #bold?
          False        #italic?
          ),     
                                   
        customTitle =   'Default Collections',                                   
        customIcon  =   None,
        customThumb =   None                                            
)



myCollectionsVisual = FolderVisual(
      TextSettings(
          None,        #color
          False,       #bold?
          False        #italic?
          ),     
                                   
        customTitle =   'My Collections',                                   
        customIcon  =   None,
        customThumb =   None                                            
)