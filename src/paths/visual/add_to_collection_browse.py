from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.TextSettings import TextSettings
from src.li.types.FolderVisual import FolderVisual
from src.li.types.CollectionVisual import CollectionVisual
from src.li.types.CustomFileVisual import CustomFileVisual
from src.tools.addonSettings import string as st

viewStyle           =       ViewStyle.TVSHOWS


createNewFolderVisual = CustomFileVisual (
      st(825),  #title
      TextSettings(
          None,                 #color
          True,                 #bold?
          False                 #italic?
          ),
                                              
          None,                 #icon
          None                  #thumb
) 


foldersVisual = FolderVisual(
      TextSettings(
          None,        #color
          False,       #bold?
          False        #italic?
          )                                                
)


createNewCollectionVisual = CustomFileVisual (
    st(826),  #title
    TextSettings(
        None,                 #color
        True,                 #bold?
        False                 #italic?
    ),
                                              
    None,                 #icon
    None                  #thumb
) 



collectionsVisual = CollectionVisual(
    TextSettings(
        None,        #color
        False,       #bold?
        False        #italic?
    )
)