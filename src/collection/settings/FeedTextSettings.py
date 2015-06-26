import globalCollection
from src.li.visual.TextSettings import TextSettings
from src.li.visual.CountTextSettings import CountTextSettings, Location, CountType
from src.li.visual.FullTextSettings import FullTextSettings
from src.li.types.CollectionVisual import CollectionVisual
from src.li.types.VideoVisual import VideoVisual
from src.tools import addonSettings as addon



                                        #color         #bold    #italic
D_BROWSE_SOURCES = TextSettings         (None,          True,   False)
D_SETTINGS       = TextSettings         (None,          False,  False)
D_PLAY_ALL       = TextSettings         (None,          False,  False, show=False)

D_VIDEO_COUNT  = CountTextSettings    ('yellow',      False,  True, Location.MIDDLE, CountType.VIEWS)
D_VIDEO_SOURCE = TextSettings         ('tan',         False,  False)
D_VIDEO_TITLE  = TextSettings         ('seashell',    False,  False)

# D_VIDEO_COUNT    = CountTextSettings    ('yellow',      False,  True, Location.MIDDLE, CountType.VIEWS)
# #D_VIDEO_SOURCE   = TextSettings         ('red',         False,  False)
# D_VIDEO_SOURCE  = TextSettings         ('chocolate',   False,  False)
# D_VIDEO_TITLE    = TextSettings         (None,          False,  False)

D_USE = False



#cannot be set by user at the moment, maybe in the future add it
BROWSE_SOURCES_TEXT  = addon.string(430)
BROWSE_SOURCES_ICON  = None
BROWSE_SOURCES_THUMB = None

SETTINGS_TEXT  = addon.string(431)
SETTINGS_ICON  = None
SETTINGS_Thumb = None

PLAY_ALL_TEXT  =  addon.string(432)
PLAY_ALL_ICON  =  'special://home/addons/plugin.video.collections/resources/media/play.png'
PLAY_ALL_THUMB =  'special://home/addons/plugin.video.collections/resources/media/play.png'






gfTS = None
class FeedTextSettings(object):
    def __init__(self, browseSourcesTS, settingsTS, playAllTS, videoFTS, use):
        self._browseSourcesTS = browseSourcesTS
        self._settingsTS = settingsTS
        self._playAllTS = playAllTS
        self._videoFTS = videoFTS
                
        self.use = use
        
        
        
    def browseSourcesTS(self):
        return self._browseSourcesTS if self.use else gfTS.browseSourcesTS()

    def settingsTS(self):
        return self._settingsTS if self.use else gfTS.settingsTS()

    def playAllTS(self):
        return self._playAllTS if self.use else gfTS.playAllTS()

    def videoFTS(self):
        return self._videoFTS if self.use else gfTS.videoFTS()
    
    
    
    def browseSourcesVisuals(self):
        title = self.browseSourcesTS().apply(BROWSE_SOURCES_TEXT)
        return title, BROWSE_SOURCES_ICON, BROWSE_SOURCES_THUMB
        
    
    
    def settingsVisuals(self):
        title = self.settingsTS().apply(SETTINGS_TEXT)
        return title, SETTINGS_ICON, SETTINGS_Thumb
    
    
    def playAllVisual(self):
        return CollectionVisual(self.playAllTS(), PLAY_ALL_TEXT, PLAY_ALL_ICON, PLAY_ALL_THUMB)           
    
    def videosVisual(self):
        return VideoVisual(self.videoFTS())




    
    def setBrowseSources(self, TS):
        self._browseSourcesTS = TS
    
    def setSettings(self, TS):
        self._settingsTS = TS
        
    def setPlayAll(self, TS):
        self._playAllTS = TS
        
    def setVideo(self, FTS):
        self._videoFTS = FTS
        
    def setUse(self, state):
        self.use = state
        
    







def init():
    global gfTS
    
    if gfTS is None:
        gc = globalCollection.gc()
        gfTS = gc.feedSettings.TS










def fromSeperated(browseSourcesTS, settingsTS, playAllTS, videoCountTS, videoSourceTS, videoTitleTS, use):    
    videoFTS = FullTextSettings(videoTitleTS, videoSourceTS, videoCountTS)
    return FeedTextSettings(browseSourcesTS, settingsTS, playAllTS, videoFTS, use)
    
    
def defaultVideoFTS():
    return FullTextSettings(D_VIDEO_TITLE, D_VIDEO_SOURCE, D_VIDEO_COUNT)
    

    
def default():     
    videoFTS = defaultVideoFTS()
    return FeedTextSettings(D_BROWSE_SOURCES, D_SETTINGS, D_PLAY_ALL, videoFTS, D_USE)

    
    
    
    
    
    
    

    
    
#         self._browseSourcesTS2 = browseSourcesTS2
#         self._settingsTS2 = settingsTS2
#         self._playAllTS2 = playAllTS2
#         self._videoFTS2 = videoFTS2    
        
        
#     def browseSourcesTS2(self):
#         if not self.use:
#             return gfTS.browseSourcesTS2()
#                 
#         return self._browseSourcesTS2 if self.useTitle2 else self._browseSourcesTS
#     
#     def settingsTS2(self):
#         if not self.use:
#             return gfTS.settingsTS2()
#                 
#         return self._settingsTS2 if self.useTitle2 else self._settingsTS
#     
#     def playAllTS2(self):
#         if not self.use:
#             return gfTS.playAllTS2()
#                 
#         return self._playAllTS2 if self.useTitle2 else self._playAllTS
#     
#     def feedFTS2(self):
#         if not self.use:
#             return gfTS.feedFTS2()
#                 
#         return self._feedFTS2 if self.useTitle2 else self._feedFTS 