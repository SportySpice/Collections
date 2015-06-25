from src.gui.SettingsWindow import SettingsWindow
from src.gui.Tab import Tab
from src.gui.ListItemTable import ListItemTable
from src.collection import Collection
from src.collection.settings import globalCollection
from src.collection.Collection import OnCollectionClick as occ
from src.collection.CollectionSource import OnSourceClick as osc
from src.collection import Collection as c
from src.collection.settings import FeedSettings as FS
from src.collection.settings import FeedTextSettings as FTS
from src.collection.settings import SourcesSettings as SS
from src.collection.settings import SourcesTextSettings as STS
from src.videosource.Video import OnVideoClick as ovc
from src.li.visual.ViewStyle import ViewStyle as vs
from src.li.visual.TextSettings import italic
from src.tools.dialog import dialog
from src.paths import remove_from_collection 
import xbmc
from src.tools.addonSettings import string as st





#general
COLLECTION_CLICK_OPTIONS        =   (None,                  occ.FEED,       occ.SOURCES,        occ.SOURCES_ONLY,       occ.PLAYALL)
COLLECTION_CLICK_LABELS         =   (st(520),               st(521),        st(522),            st(523),                st(524))

GLOBAL_COLLECTION_CLICK_OPTIONS =                           (occ.FEED,      occ.SOURCES,        occ.SOURCES_ONLY,       occ.PLAYALL)
GLOBAL_COLLECTION_CLICK_LABELS  =                           (st(521),       st(522),            st(523),                st(524))


#feed
VIEW_STYLE_OPTIONS = (vs.FILES, vs.SONGS,   vs.ARTISTS, vs.ALBUMS,  vs.MOVIES,  vs.TVSHOWS, vs.EPISODES,    vs.MUSICVIDEOS)
VIEW_STYLE_LABELS  = (st(610),  st(611),    st(612),    st(613),    st(614),    st(615),    st(616),        st(617)       )
                 
VIDEO_CLICK_OPTIONS = (ovc.PLAY_ONLY,           ovc.PLAY_QUEUE_REST)
VIDEO_CLICK_LABELS  = (st(620),                 st(621)            )

COLLECTION_LIMIT_VALUES = list(range(10,201,10))
SOURCE_LIMIT_VALUES     = list(range(1,51))


#sources
SOURCE_CLICK_KODI_OPTIONS   = (osc.BROWSE,  osc.PLAYALL,    osc.BROWSE_ORIGIN)
SOURCE_CLICK_KODI_LABELS    = (st(570),     st(571),        st(572)          )

SOURCE_CLICK_YT_OPTIONS     = (osc.BROWSE, osc.PLAYALL)
SOURCE_CLICK_YT_LABELS      = (st(570),    st(571)    )


def edit(collectionFile=None):    
    if not collectionFile:
        collection = globalCollection.gc()
        globalC = True
        windowTitle = st(500)
        
    else:
        collection = Collection.fromFile(collectionFile)
        globalC = False
        windowTitle = collection.title
        
    def saveCallback():
        collection.writeCollectionFile()
        xbmc.executebuiltin('XBMC.Container.Refresh()')
    
    window = SettingsWindow(windowTitle, saveCallback=saveCallback)
    
     
    generalTab = Tab( st(501) )
    generalTab.addEmptyRow()
    
    if globalC:
        clickOptions = GLOBAL_COLLECTION_CLICK_OPTIONS
        clickLabels = GLOBAL_COLLECTION_CLICK_LABELS  
        clickDefault = c.D_ONCLICK
    else:
        clickOptions = COLLECTION_CLICK_OPTIONS
        clickLabels = COLLECTION_CLICK_LABELS        
        clickDefault = None
        generalTab.addInputButton(  st(510),                        collection.title,       collection.title,   lambda title: collection.setTitle(title))
        
    generalTab.addEnum(             st(515),    clickOptions,       collection._onClick,    clickDefault,       lambda value: collection.setOnClick(value), customLabels=clickLabels)
    
    if not globalC:
        generalTab.addButton(st(516), lambda: removeSourceWindow(collection), bold=False)
        generalTab.addEmptyRow()
        generalTab.addButton(st(517), lambda: switchToGlobalSettings(window), bold=False)
        
    
    
    feedTab = Tab( st(502) )
    fs = collection.feedSettings
    
    if not globalC:    
        feedTab.addUseGlobalButton(not fs.use, not FS.D_USE, lambda state: fs.setUse(not state))
    
    feedTab.addEmptyRow()    
    feedTab.addEnum(    st(530),    VIEW_STYLE_OPTIONS,     fs._viewStyle,      FS.D_VIEWSTYLE,     lambda value: fs.setViewStyle(value),       customLabels=VIEW_STYLE_LABELS)
    feedTab.addEnum(    st(531),    VIDEO_CLICK_OPTIONS,    fs._onVideoClick,   FS.D_VIDEOCLICK,    lambda value: fs.setOnVideoClick(value),    customLabels=VIDEO_CLICK_LABELS)
    feedTab.addBool(    st(532),                               fs._unwatched,      FS.D_UNWATCHED,     lambda value: fs.setUnwatched(value))
    
    feedTab.addEmptyRow()
    feedTab.addEnum(    st(533),    COLLECTION_LIMIT_VALUES,fs._limit,          FS.D_LIMIT,         lambda value: fs.setLimit(value))
    feedTab.addEnum(    st(534),    SOURCE_LIMIT_VALUES,    fs.sLimit,          FS.D_SLIMIT,        lambda value: fs.setSourceLimit(value))
    
    if not globalC:
        feedTab.addButton(  st(535), lambda: limitsWindow(collection), bold=False)
    


    feedTextTab = Tab( st(503), rows=18, columns=10)    
    fts = fs.TS
    
    if not globalC:           
        feedTextTab.addUseGlobalButton(not fts.use, not FTS.D_USE, lambda state: fts.setUse(not state))
    
    table = ListItemTable()         
    table.addCustomItem(    st(540),    fts._browseSourcesTS,   FTS.D_BROWSE_SOURCES,   lambda TS: fts.setBrowseSources(TS))
    table.addCustomItem(    st(541),    fts._settingsTS,        FTS.D_SETTINGS,         lambda TS: fts.setSettings(TS),         showOptions=True)
    table.addCustomItem(    st(542),    fts._playAllTS,         FTS.D_PLAY_ALL,         lambda TS: fts.setPlayAll(TS),          showOptions=True, radioPadX=0)

    table.addEmptyRow()    
    table.addFullItem(                      fts._videoFTS,          FTS.defaultVideoFTS(),  lambda FTS: fts.setVideo(FTS),          st(550), st(551), 452364, st(552), st(553))
    
    table.addEmptyRow()  
    table.addExamples()      
    feedTextTab.addListItemTable(table)
    
    
    
    
    sourcesTab = Tab( st(504) )
    ss = collection.sourcesSettings
    
    if not globalC:
        sourcesTab.addUseGlobalButton(not ss.use, not SS.D_USE, lambda state: ss.setUse(not state))
    
    sourcesTab.addEmptyRow()    
    sourcesTab.addEnum( st(560),    VIEW_STYLE_OPTIONS,         ss._viewStyle,          SS.D_VIEWSTYLE,         lambda value: ss.setViewStyle(value),       customLabels=VIEW_STYLE_LABELS)
    sourcesTab.addEmptyRow()
    
    sourcesTab.addEnum( st(561),    SOURCE_CLICK_KODI_OPTIONS,  ss.onSourceClickKodi,   SS.D_SOURCE_CLICK_KODI, lambda value: ss.setSourceClickKodi(value), customLabels=SOURCE_CLICK_KODI_LABELS)
    sourcesTab.addEnum( st(562),    SOURCE_CLICK_YT_OPTIONS,    ss.onSourceClickYt,     SS.D_SOURCE_CLICK_YT,   lambda value: ss.setSourceClickYt(value),   customLabels=SOURCE_CLICK_YT_LABELS)
    
    if not globalC:
        sourcesTab.addButton( st(563), lambda: sourceClickWindow(collection), bold=False)
    
    
    sourcesTextTab = Tab( st(505) , rows=18, columns=10)        
    sts = ss.TS   
    
    if not globalC:
        sourcesTextTab.addUseGlobalButton(not sts.use, not STS.D_USE, lambda state: sts.setUse(not state))
             
    table = ListItemTable()
    table.addCustomItem(st(580),   sts._cSourceTS,   STS.D_CSOURCE,   lambda TS: sts.setCSource(TS))    
    table.addEmptyRow()    
    table.addExamples()
    
    sourcesTextTab.addListItemTable(table)
    
    
    window.addTabs([generalTab, feedTab, feedTextTab, sourcesTab, sourcesTextTab])
    
    
    
    
    xbmc.executebuiltin('XBMC.Dialog.Close(all, true)')
    window.show()
    window.delete()
    
    
    


def removeSourceWindow(collection):
#     window = SettingsWindow('Remove Source', width=500, height=550, hideTabs=True, showButtons=False)
#     tab = Tab('Remove')
#     
#     def onClick(cSource):
#         if remove_from_collection.removeDirect(cSource, refreshContainer=False):
#             window.close()
#     
#     for cSource in collection.cSources:
#         tab.addButton(cSource.videoSource.title, lambda cSource=cSource: onClick(cSource), columnSpan=8, centered=False)
#         
#     window.addTabs([tab])
#     
#     window.show()
#     window.delete()
    
    selectedIndex = dialog.select(st(516), list(cSource.videoSource.title for cSource in collection.cSources))
    if selectedIndex == -1:
        return
    
    remove_from_collection.removeDirect(collection.cSources[selectedIndex], refreshContainer=False)
    
    
    
    
USE_MAIN_TEXT = italic(st(606))

def limitsWindow(collection):
    window = SettingsWindow(st(534), width=600, height=550, hideTabs=True)
    tab = Tab('')
    
    
    
    values = [None]                  
    labels = [USE_MAIN_TEXT]
    
    values.extend(SOURCE_LIMIT_VALUES)
    labels.extend(SOURCE_LIMIT_VALUES)
    
    
    for cSource in collection.cSources:
        tab.addEnum(cSource.videoSource.title,         values,      cSource._limit,          None,        lambda value, cSource=cSource: cSource.setLimit(value), customLabels=labels)
    
    
    window.addTabs([tab])
    
    window.show()
    window.delete()
    
    
    
def sourceClickWindow(collection):
    window = SettingsWindow(st(565), width=600, height=550, hideTabs=True)
    tab = Tab('')
    
    kodiValues = [None]                  
    kodiLabels = [USE_MAIN_TEXT]    
    kodiValues.extend(SOURCE_CLICK_KODI_OPTIONS)
    kodiLabels.extend(SOURCE_CLICK_KODI_LABELS)
    
    ytValues = [None]                  
    ytLabels = [USE_MAIN_TEXT]    
    ytValues.extend(SOURCE_CLICK_YT_OPTIONS)
    ytLabels.extend(SOURCE_CLICK_YT_LABELS)
    
    
    for cSource in collection.cSources:
        if cSource.isKodiFolder():
            values = kodiValues
            labels = kodiLabels
        else:
            values = ytValues
            labels = ytLabels
            
        tab.addEnum(cSource.videoSource.title,         values,      cSource._onClick,          None,        lambda value, cSource=cSource: cSource.setOnClick(value), customLabels=labels)
    
    
    window.addTabs([tab])
    
    window.show()
    window.delete()
    
    
def switchToGlobalSettings(currentWindow):
    currentWindow.close()
    edit()