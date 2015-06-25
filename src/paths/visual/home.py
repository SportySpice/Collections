from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.TextSettings import TextSettings
from src.li.types.FolderVisual import FolderVisual
from src.li.types.CustomFolderVisual import CustomFolderVisual


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

browseForSourcesVisual = CustomFolderVisual(
      'Browse For Sources',
      TextSettings(
          None,        #color
          False,       #bold?
          False        #italic?
          ),     
                                   
        None,       #icon
        None,       #thumb                                 
)