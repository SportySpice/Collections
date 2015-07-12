from src.gui.SettingsWindow import SettingsWindow
from src.gui.Tab import Tab
from src.gui.ListItemTable import ListItemTable
from src.collection import Collection
from src.collection.settings import globalCollection
from src.collection.Collection import OnCollectionClick as occ
from src.collection.CollectionSource import OnSourceClick as osc
from src.collection import Collection as c
from src.videosource.kodi.FolderVideo import ParseMethod as pm
from src.collection.settings import FeedSettings as FS
from src.collection.settings import FeedTextSettings as FTS
from src.collection.settings import SourcesSettings as SS
from src.collection.settings import SourcesTextSettings as STS
from src.collection.settings import FolderSettings as FDS
from src.videosource.VideoList import VideoSort as vsr, VideoCountType as vct, vsToCounts
from src.videosource.Video import OnVideoClick as ovc
from src.li.visual.ViewStyle import ViewStyle as vs
from src.li.visual.TextSettings import italic
from src.tools.dialog import dialog
from src.paths import remove_from_collection 
from src.tools import xbmcTool
from src.tools.addonSettings import string as st






#general
COLLECTION_CLICK_OPTIONS        =   (None,                  occ.FEED,       occ.SOURCES,        occ.SOURCES_ONLY,       occ.PLAYALL)
COLLECTION_CLICK_LABELS         =   (st(520),               st(521),        st(522),            st(523),                st(524))

GLOBAL_COLLECTION_CLICK_OPTIONS =                           (occ.FEED,      occ.SOURCES,        occ.SOURCES_ONLY,       occ.PLAYALL)
GLOBAL_COLLECTION_CLICK_LABELS  =                           (st(521),       st(522),            st(523),                st(524))


#feed
VIEW_STYLE_OPTIONS = (vs.FILES, vs.SONGS,   vs.ARTISTS, vs.ALBUMS,  vs.MOVIES,  vs.TVSHOWS, vs.EPISODES,    vs.MUSICVIDEOS)
VIEW_STYLE_LABELS  = (st(610),  st(611),    st(612),    st(613),    st(614),    st(615),    st(616),        st(617)       )

VIDEO_SORT_OPTIONS  = (vsr.DATE, vsr.VIEWS,  vsr.DURATION,      vsr.POSITION,       vsr.SHUFFLE,    vsr.SOURCE_TITLE,   vsr.VIDEO_TITLE,    vsr.RATING, vsr.LIKES,  vsr.DISLIKES,   vsr.COMMENTS,   vsr.PLAYCOUNT,  vsr.LASTPLAYED)
VIDEO_SORT_LABELS   = (st(620),  st(621),    st(622),           st(623),            st(624),        st(625),            st(626),            st(628),    st(629),    st(630),        st(631),        st(632),        st(633)       )

VIDEO_SORT2_OPTIONS = ( None    ,)  + VIDEO_SORT_OPTIONS[:4] + VIDEO_SORT_OPTIONS[5:]   #all except shuffle, be careful
VIDEO_SORT2_LABELS  = ( st(607) ,)  + VIDEO_SORT_LABELS [:4] + VIDEO_SORT_LABELS [5:]   #when making changes

VIDEO_COUNT_OPTIONS = (vct.DATE,    vct.VIEWS,  vct.DURATION,   vct.POSITION,   vct.RATING, vct.LIKES,  vct.DISLIKES,   vct.COMMENTS,   vct.PLAYCOUNT,  vct.LASTPLAYED)
VIDEO_COUNT_LABELS  = (st(640),     st(641),    st(642),        st(643),        st(644),    st(645),    st(646),        st(647),        st(648),        st(649)       )     

VIDEO_COUNT2_OPTIONS = ( None    ,)  + VIDEO_COUNT_OPTIONS
VIDEO_COUNT2_LABELS  = ( st(607) ,)  + VIDEO_COUNT_LABELS

                 
VIDEO_CLICK_OPTIONS = (ovc.PLAY_ONLY,           ovc.PLAY_QUEUE_REST)
VIDEO_CLICK_LABELS  = (st(660),                 st(661)            )

COLLECTION_LIMIT_VALUES = tuple( range(10,200,10) + range(200, 500, 50) + range(500, 1000, 100) + range(1000, 2001, 200))
SOURCE_LIMIT_VALUES     = tuple(range(1,51))



#sources
SOURCE_CLICK_KODI_OPTIONS   = (osc.BROWSE,  osc.PLAYALL,    osc.BROWSE_ORIGIN)
SOURCE_CLICK_KODI_LABELS    = (st(580),     st(581),        st(582)          )

SOURCE_CLICK_YT_OPTIONS     = (osc.BROWSE, osc.PLAYALL)
SOURCE_CLICK_YT_LABELS      = (st(580),    st(581)    )


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
        xbmcTool.refreshContainer()
    
    window = SettingsWindow(windowTitle, saveCallback=saveCallback, width=800, height=560)
    
    
######GENERAL TAB######     
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
        generalTab.addEmptyRow()
        generalTab.addButton(st(516), lambda: useInFeedWindow(collection),      bold=False, columnSpan=4)
        generalTab.addButton(st(517), lambda: removeSourceWindow(collection),   bold=False, columnSpan=4)        
        generalTab.addButton(st(518), lambda: switchToGlobalSettings(window),   bold=False, columnSpan=4)
        
    
    
######FEED TAB######     
    feedTab = Tab( st(502) )
    fs = collection.feedSettings
    
    if not globalC:    
        feedTab.addUseGlobalButton(not fs.use, not FS.D_USE, lambda state: fs.setUse(not state))
    
    feedTab.addEmptyRow()    
    feedTab.addEnum(    st(530),    VIEW_STYLE_OPTIONS,     fs._viewStyle,      FS.D_VIEWSTYLE,     lambda value: fs.setViewStyle(value),       customLabels=VIEW_STYLE_LABELS)
    feedTab.addEnum(    st(531),    VIDEO_CLICK_OPTIONS,    fs._onVideoClick,   FS.D_VIDEOCLICK,    lambda value: fs.setOnVideoClick(value),    customLabels=VIDEO_CLICK_LABELS)
    feedTab.addBool(    st(532),                            fs._unwatched,      FS.D_UNWATCHED,     lambda value: fs.setUnwatched(value))
    
    feedTab.addEmptyRow()
    
    def sortChange(vs):        
        vct1, vct2 = vsToCounts[vs]
        count1Button.update(vct1)
        count2Button.update(vct2)
        
    
    feedTab.addEnum                 (   st(533),    VIDEO_SORT_OPTIONS,     fs._sort,           FS.D_SORT,          lambda value: fs.setSort(value),            customLabels=VIDEO_SORT_LABELS,      changeCallback=sortChange)
    feedTab.addEnum                 (   st(534),    VIDEO_SORT2_OPTIONS,    fs._sort2,          FS.D_SORT2,         lambda value: fs.setSort2(value),           customLabels=VIDEO_SORT2_LABELS)
    feedTab.addBool                 (   st(535),                            fs._reverseSort,    FS.D_REVERSE_SORT,  lambda value: fs.setReverseSort(value))
    count1Button = feedTab.addEnum  (   st(536),    VIDEO_COUNT_OPTIONS,    fs._countType,      FS.D_COUNT_TYPE,    lambda value: fs.setCountType(value),       customLabels=VIDEO_COUNT_LABELS)
    count2Button = feedTab.addEnum  (   st(537),    VIDEO_COUNT2_OPTIONS,   fs._countType2,     FS.D_COUNT_TYPE2,   lambda value: fs.setCountType2(value),      customLabels=VIDEO_COUNT2_LABELS)
    #feedTab.addBool(    st(534),                            fs._replaceViews,   FS.D_REPLACE_VIEWS, lambda value: fs.setReplaceViews(value))
    
    
    
    
    
    
    
 

######FEED LIMITS TAB######
    flTab = Tab( st(503) )
    if not globalC:    
        flTab .addUseGlobalButton(not fs.useLimits, not FS.D_USELIMITS, lambda state: fs.setUseLimits(not state))
    
    
    flTab .addEmptyRow()
    flTab .addEnum(     st(540),    COLLECTION_LIMIT_VALUES,fs._limit,          FS.D_LIMIT,         lambda value: fs.setLimit(value))
    flTab .addEnum(     st(541),    SOURCE_LIMIT_VALUES,    fs.sLimit,          FS.D_SLIMIT,        lambda value: fs.setSourceLimit(value))
    
    if not globalC:
        flTab .addButton(  st(542), lambda: limitsWindow(collection), bold=False)
        
    flTab .addEmptyRow()
    flTab .addEnum(     st(543),    (None,),                None,               None,               lambda value: value,                            customLabels=('Coming Soon',))
    flTab .addEnum(     st(544),    (None,),                None,               None,               lambda value: value,                            customLabels=('Coming Soon',))    
    


######FEED TEXT TAB######
    feedTextTab = Tab( st(504), rows=20, columns=10)    
    fts = fs.TS
    
    if not globalC:           
        feedTextTab.addUseGlobalButton(not fts.use, not FTS.D_USE, lambda state: fts.setUse(not state))
    
    table = ListItemTable()         
    table.addCustomItem(    st(550),    fts._browseSourcesTS,   FTS.D_BROWSE_SOURCES,   lambda TS: fts.setBrowseSources(TS))
    table.addCustomItem(    st(551),    fts._settingsTS,        FTS.D_SETTINGS,         lambda TS: fts.setSettings(TS),         showOptions=True)
    table.addCustomItem(    st(552),    fts._sortTS,            FTS.D_SORT,             lambda TS: fts.setSort(TS),             showOptions=True)
    table.addCustomItem(    st(553),    fts._playAllTS,         FTS.D_PLAY_ALL,         lambda TS: fts.setPlayAll(TS),          showOptions=True, radioPadX=0)

    table.addEmptyRow()    
    table.addFullItem(                      fts._videoFTS,          FTS.defaultVideoFTS(),  lambda FTS: fts.setVideo(FTS),          st(560), st(561), st(562), st(563))
    
    table.addEmptyRow()  
    table.addExamples()      
    feedTextTab.addListItemTable(table)
    
    
    
######SOURCES TAB######    
    sourcesTab = Tab( st(505) )
    ss = collection.sourcesSettings
    
    if not globalC:
        sourcesTab.addUseGlobalButton(not ss.use, not SS.D_USE, lambda state: ss.setUse(not state))
    
    sourcesTab.addEmptyRow()    
    sourcesTab.addEnum( st(570),    VIEW_STYLE_OPTIONS,         ss._viewStyle,          SS.D_VIEWSTYLE,         lambda value: ss.setViewStyle(value),       customLabels=VIEW_STYLE_LABELS)
    sourcesTab.addEmptyRow()
    
    sourcesTab.addEnum( st(571),    SOURCE_CLICK_KODI_OPTIONS,  ss.onSourceClickKodi,   SS.D_SOURCE_CLICK_KODI, lambda value: ss.setSourceClickKodi(value), customLabels=SOURCE_CLICK_KODI_LABELS)
    sourcesTab.addEnum( st(572),    SOURCE_CLICK_YT_OPTIONS,    ss.onSourceClickYt,     SS.D_SOURCE_CLICK_YT,   lambda value: ss.setSourceClickYt(value),   customLabels=SOURCE_CLICK_YT_LABELS)
    
    if not globalC:
        sourcesTab.addButton( st(573), lambda: sourceClickWindow(collection), bold=False)
    
    
    
######SOURCES TEXT TAB######
    sourcesTextTab = Tab( st(506) , rows=18, columns=10)        
    sts = ss.TS   
    
    if not globalC:
        sourcesTextTab.addUseGlobalButton(not sts.use, not STS.D_USE, lambda state: sts.setUse(not state))
             
    table = ListItemTable()
    table.addCustomItem(st(585),   sts._cSourceTS,   STS.D_CSOURCE,   lambda TS: sts.setCSource(TS))    
    table.addEmptyRow()    
    table.addExamples()
    
    sourcesTextTab.addListItemTable(table)
    
    
######FOLDER SETTINGS TAB######
    folderSettingsTab = Tab( st(507) )        
    fds = collection.folderSettings
    
    if not globalC:
        folderSettingsTab.addUseGlobalButton(not fds.use, not FDS.D_USE, lambda state: fds.setUse(not state))
    
    folderSettingsTab.addEmptyRow()
    folderSettingsTab.addBool(      st(590), fds.estimateDates, FDS.D_ESTIMATE_DATES, lambda state: fds.setEstimateDates(state))
    
    if not globalC:
        folderSettingsTab.addButton( st(591), lambda: estimateDatesWindow(collection),  bold=False)
        folderSettingsTab.addEmptyRow()
        folderSettingsTab.addButton( st(592), lambda: parseMethodWindow(collection),    bold=False)
    
    
    
    
    window.addTabs([generalTab, feedTab, flTab, feedTextTab, sourcesTab, sourcesTextTab, folderSettingsTab])
    xbmcTool.closeOpenDialogs()
    window.show()
    window.delete()
    
    

    
    
    
    
def useInFeedWindow(collection):
    window = SettingsWindow(st(516), width=500, height=550, hideTabs=True)
    tab = Tab('')
        
     
    
    for cSource in collection.cSources:
        tab.addBoolFullSpan(cSource.title(),         cSource.useInFeed,      True, lambda value, cSource=cSource: cSource.setUseInFeed(value))
    
    
    window.addTabs([tab])
    
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
#         tab.addButton(cSource.title(), lambda cSource=cSource: onClick(cSource), columnSpan=8, centered=False)
#         
#     window.addTabs([tab])
#     
#     window.show()
#     window.delete()
    
    selectedIndex = dialog.select(st(517), list(cSource.title() for cSource in collection.cSources))
    if selectedIndex == -1:
        return
    
    remove_from_collection.removeDirect(collection.cSources[selectedIndex], refreshContainer=False)
    
    
    
    
USE_MAIN_TEXT = italic(st(606))

def limitsWindow(collection):
    window = SettingsWindow(st(541), width=600, height=550, hideTabs=True)
    tab = Tab('')
    
    
    
    values = (None,)             +   SOURCE_LIMIT_VALUES        
    labels = (USE_MAIN_TEXT,)    +   SOURCE_LIMIT_VALUES
    
    
    for cSource in collection.cSources:
        tab.addEnum(cSource.title(),         values,      cSource._limit,          None,        lambda value, cSource=cSource: cSource.setLimit(value), customLabels=labels)
    
    
    window.addTabs([tab])
    
    window.show()
    window.delete()
    
    
    
def sourceClickWindow(collection):
    window = SettingsWindow(st(575), width=600, height=550, hideTabs=True)
    tab = Tab('')
    
    kodiValues = (None,)            +   SOURCE_CLICK_KODI_OPTIONS
    kodiLabels = (USE_MAIN_TEXT,)   +   SOURCE_CLICK_KODI_LABELS
    
    ytValues = (None,)              +   SOURCE_CLICK_YT_OPTIONS
    ytLabels = (USE_MAIN_TEXT,)     +   SOURCE_CLICK_YT_LABELS
    
    
    for cSource in collection.cSources:
        if cSource.isKodiFolder():
            values = kodiValues
            labels = kodiLabels
        else:
            values = ytValues
            labels = ytLabels
            
        tab.addEnum(cSource.title(),         values,      cSource._onClick,          None,        lambda value, cSource=cSource: cSource.setOnClick(value), customLabels=labels)
    
    
    window.addTabs([tab])
    
    window.show()
    window.delete()
    
    
def estimateDatesWindow(collection):
    window = SettingsWindow(st(590), width=600, height=550, hideTabs=True)
    tab = Tab('')

    values = (None,             True,       False)          
    labels = (USE_MAIN_TEXT,    st(608),    st(609))    
    
    for cSource in collection.cSourcesKodi:
        tab.addEnum(cSource.title(),         values,      cSource._estimateDates,          None,        lambda value, cSource=cSource: cSource.setEstimateDates(value), customLabels=labels)
    
    
    window.addTabs([tab])
    
    window.show()
    window.delete()
    
    
def parseMethodWindow(collection):
    window = SettingsWindow(st(593), width=600, height=550, hideTabs=True)
    tab = Tab('')
        
    
    values = (pm.NORMAL,        pm.FIRST_IN_FOLDER  )     #pm.FOLDERS_AS_VIDEOS          
    labels = (st(595),          st(596),            )     #st(597)    
    
    for cSource in collection.cSourcesKodi:
        tab.addEnum(cSource.title(),         values,      cSource.parseMethod,          None,        lambda value, cSource=cSource: cSource.setParseMethod(value), customLabels=labels)
    
    
    window.addTabs([tab])
    
    window.show()
    window.delete()
    
    
def switchToGlobalSettings(currentWindow):
    currentWindow.close()
    edit()