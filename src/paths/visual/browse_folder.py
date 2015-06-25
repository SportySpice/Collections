from src.li.visual.ViewStyle import ViewStyle
from src.li.visual.TextSettings import TextSettings
from src.li.types.FolderVisual import FolderVisual
from src.li.types.CollectionVisual import CollectionVisual

viewStyle           =       ViewStyle.TVSHOWS


foldersVisual = FolderVisual(
      TextSettings(
          None,        #color
          False,       #bold?
          False        #italic?
          )                                                
)



collectionsVisual = CollectionVisual(
      TextSettings(
          None,        #color
          False,       #bold?
          False        #italic?
          ),     
)