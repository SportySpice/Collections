from src.li.visual.TextSettings import TextSettings
from src.li.types.CollectionVisual import CollectionVisual
from src.collection.settings import SourcesTextSettings as STS

feedVisual = CollectionVisual(
    TextSettings(
        None,        #color
        True,       #bold?
        False        #italic?
    ),     
    customTitle = STS.FEED_TEXT
)