import strings as st
import src.collection.Collection as c
from src.collection.csource import KodiCollectionSource as KCS
from src.collection.settings import FeedSettings as FS
from src.collection.settings import FeedTextSettings as FTS
from src.collection.settings import SourcesSettings as SS
from src.collection.settings import SourcesTextSettings as STS
from src.collection.settings import FolderSettings as FDS
from src.cxml.OrderedNode import OrderedNode
from src.cxml.OrderedTextRow import OrderedTextRow
from src.videosource.VideoSource import SourceType
from src.cxml import exporter as xmlExporter
from src.cxml.OrderedSettings import OrderedSettings


def export(collection):
    collectionSettings = OrderedSettings()            
    collectionSettings.addIfNotNone(    st.ON_CLICK,             collection._onClick,                   customValueDic=st.occToValue)
    collectionSettings.addIfDifferent(  st.COLLECTION_DEFAULT,   collection.default,    c.D_DEFAULT)
    
        
    rootNode = OrderedNode(st.COLLECTION_NODE, collectionSettings, collection.title)        
    nodeList = []
    
    
    
        
    
    nodeDic = {}
    options = {SourceType.CHANNEL:_processChannel, SourceType.PLAYLIST:_processPlaylist, 
               SourceType.FOLDER:_processKodiFolder}
    
    for cSource in collection.cSources:
        s = OrderedSettings()
        
        vSource = cSource.videoSource
        nodeName, textRow =  options[vSource.type](cSource, vSource, s)
        
        s.addIfNotNone( st.ON_CLICK,                cSource._onClick,       customValueDic=st.oscToValue)
        s.addIfFalse  ( st.CSOURCE_USE_IN_FEED,     cSource.useInFeed)                    
        s.addIfNotNone( st.CSOURCE_LIMIT,           cSource._limit)
        s.addIfNotNone( st.CSOURCE_CUSTOM_TITLE,    cSource.customTitle)
        s.addIfNotNone( st.CSOURCE_CUSTOM_THUMB,    cSource.customThumb)
        
        if nodeName in nodeDic:
            node = nodeDic[nodeName]
        else:
            node = OrderedNode(nodeName)
            nodeDic[nodeName] = node
            nodeList.append(node)
            
        node.addTextRow(textRow)
                    
    
    feedNode            = _processFeedSettings(collection)
    sourcesNode         = _processSourcesSettings(collection)
    folderSettingsNode  = _processFolderSettings(collection) 
    
    if feedNode or sourcesNode or folderSettingsNode:
        views = OrderedNode(st.VIEWS_NODE)        
        if feedNode:            views.addChild(feedNode)
        if sourcesNode:         views.addChild(sourcesNode)
        if folderSettingsNode:  views.addChild(folderSettingsNode)
        
        nodeList.append(views)
    
    
    rootNode.addChildren(nodeList)
    xmlExporter.export(rootNode, collection.file)
                    
                 
                 
                 
                 
                 
                    
def _processChannel(ytCSource, channel, sourceSettings):    
    if channel.username:
        text = channel.username
        comment = None
        
    else:
        text = channel.channelId
        sourceSettings.add(st.CHANNEL_ID, True)
        comment = channel.title
    
    return st.CHANNELS_NODE, OrderedTextRow(text, sourceSettings, comment=comment)



def _processPlaylist(ytCSource, playlist, sourceSettings):
    text = playlist.playlistId   
    comment =  playlist.title
    
    return st.PLAYLISTS_NODE, OrderedTextRow(text, sourceSettings, comment=comment)



def _processKodiFolder(kodiCSource, folder, sourceSettings):
    text = folder.path
    
    sourceSettings.addIfDifferent(  st.FOLDER_PARSE_METHOD,     kodiCSource.parseMethod,        KCS.D_PARSE_METHOD,     customValueDic=st.pmToValue)
    sourceSettings.addIfNotNone(    st.FOLDER_ESTIMATE_DATES,   kodiCSource._estimateDates)
    #sourceSettings.add('title', folder.title)
    
    return st.FOLDERS_NODE, OrderedTextRow(text, sourceSettings)






def _processTS(name, TS, defaultTS, returnSettings=False):
    s = OrderedSettings()
    
    s.addIfDifferent(   st.TS_COLOR,   TS.color,   defaultTS.color)
    s.addIfDifferent(   st.TS_BOLD,    TS.bold,    defaultTS.bold)
    s.addIfDifferent(   st.TS_ITALIC,  TS.italic,  defaultTS.italic)
    s.addIfDifferent(   st.TS_SHOW,    TS.show,    defaultTS.show)
    
    if returnSettings:
        return s
    
    
    if not s.hasValues():
        return None
    
    return OrderedTextRow(name, s)
        
    


# def _processCTS(name, CTS, defaultCTS):
#     s = _processTS(name, CTS, defaultCTS, returnSettings=True)
#     s.addIfDifferent(   st.CTS_LOACTION,    CTS.location,   defaultCTS.location,        customValueDic=st.locToValue)
# 
# 
#     if not s.hasValues():
#         return None
#     
#     return OrderedTextRow(name, s)




def _processFeedSettings(collection):
    ns = OrderedSettings()
    fs = collection.feedSettings
    fts = fs.TS
    videoFTS = fts._videoFTS

    ns.addIfDifferent(  st.VIEWSTYLE,       fs._viewStyle,      FS.D_VIEWSTYLE)
    ns.addIfDifferent(  st.FEED_SORT,       fs._sort,           FS.D_SORT,              customValueDic=st.vsrToValue)
    ns.addIfDifferent(  st.FEED_SORT2,      fs._sort2,          FS.D_SORT2,             customValueDic=st.vsrToValue,   nonePossible=True)
    ns.addIfDifferent(  st.FEED_REVSORT,    fs._reverseSort,    FS.D_REVERSE_SORT)
    ns.addIfDifferent(  st.FEED_COUNT_TYPE, fs._countType,      FS.D_COUNT_TYPE,        customValueDic=st.vctToValue)
    ns.addIfDifferent(  st.FEED_COUNT_TYPE2,fs._countType2,     FS.D_COUNT_TYPE2,       customValueDic=st.vctToValue,   nonePossible=True)
    #ns.addIfDifferent(  st.FEED_REPVIEWS,   fs._replaceViews,   FS.D_REPLACE_VIEWS)
    ns.addIfDifferent(  st.FEED_VIDEOCLICK, fs._onVideoClick,   FS.D_VIDEOCLICK,        customValueDic=st.ovcToValue)    
    ns.addIfDifferent(  st.FEED_UNWATCHED,  fs._unwatched,      FS.D_UNWATCHED)
    ns.addIfDifferent(  st.FEED_LIMIT,      fs._limit,          FS.D_LIMIT)
    ns.addIfDifferent(  st.FEED_SLIMIT,     fs.sLimit,          FS.D_SLIMIT)
    
    ns.addIfDifferent(  st.USE,             fs.use,             FS.D_USE)
    ns.addIfDifferent(  st.USELIMITS,       fs.useLimits,       FS.D_USELIMITS)
    ns.addIfDifferent(  st.USETS,           fts.use,            FTS.D_USE)
    
    ns.addIfDifferent(  st.COUNT_LOACTION,  videoFTS.countLocation,  FTS.D_COUNT_LOCATION,   customValueDic=st.locToValue)
    
    browseSourcesTR =   _processTS( st.FEED_TR_BROWSE_SOURCES,  fts._browseSourcesTS,   FTS.D_BROWSE_SOURCES    )
    settingsTR      =   _processTS( st.FEED_TR_SETTINGS,        fts._settingsTS,        FTS.D_SETTINGS          )
    sortTR          =   _processTS( st.FEED_TR_SORT,            fts._sortTS,            FTS.D_SORT              )
    playAllTR       =   _processTS( st.FEED_TR_PLAYALL,         fts._playAllTS,         FTS.D_PLAY_ALL          )
        
    countTR         =   _processTS(st.FEED_TR_VIDEO_COUNT,      videoFTS.countTS,       FTS.D_COUNT             )
    count2TR        =   _processTS(st.FEED_TR_VIDEO_COUNT2,     videoFTS.count2TS,      FTS.D_COUNT2            )
    videoSourceTR   =   _processTS( st.FEED_TR_VIDEO_SOURCE,    videoFTS.sourceTS,      FTS.D_VIDEO_SOURCE      )
    videoTitleTR    =   _processTS( st.FEED_TR_VIDEO_TITLE,     videoFTS.titleTS,       FTS.D_VIDEO_TITLE       )
    
    
    feedNode = OrderedNode(st.FEED_NODE, ns)
    
    if browseSourcesTR: feedNode.addTextRow(browseSourcesTR)
    if settingsTR:      feedNode.addTextRow(settingsTR)
    if sortTR:          feedNode.addTextRow(sortTR)
    if playAllTR:       feedNode.addTextRow(playAllTR)
    
    if countTR:         feedNode.addTextRow(countTR)
    if count2TR:        feedNode.addTextRow(count2TR)
    if videoSourceTR:   feedNode.addTextRow(videoSourceTR)
    if videoTitleTR:    feedNode.addTextRow(videoTitleTR)
    
    
    if (not feedNode.hasSettings()) and not (feedNode.hasTextrows()):
        return None    
        
    return feedNode

def _processSourcesSettings(collection):
    ns = OrderedSettings()
    ss = collection.sourcesSettings
    sts = ss.TS
    
    ns.addIfDifferent(  st.VIEWSTYLE,                   ss._viewStyle,          SS.D_VIEWSTYLE)
    ns.addIfDifferent(  st.SOURCES_SOURCE_CLICK_KODI,   ss.onSourceClickKodi,   SS.D_SOURCE_CLICK_KODI,     customValueDic=st.oscToValue)
    ns.addIfDifferent(  st.SOURCES_SOURCE_CLICK_YT,     ss.onSourceClickYt,     SS.D_SOURCE_CLICK_YT,       customValueDic=st.oscToValue)
    
    ns.addIfDifferent(  st.USE,             ss.use,             SS.D_USE)
    ns.addIfDifferent(  st.USETS,           sts.use,            STS.D_USE)    

        
    cSourceTR =   _processTS(st.SOURCES_TR_CSOURCE,     sts._cSourceTS,   STS.D_CSOURCE   )
    
    
    sourcesNode = OrderedNode(st.SOURCES_NODE, ns)
    if cSourceTR:   sourcesNode.addTextRow(cSourceTR)
    
    
    if (not sourcesNode.hasSettings()) and not (sourcesNode.hasTextrows()):
        return None
    
    return sourcesNode


def _processFolderSettings(collection):
    ns = OrderedSettings()
    fds = collection.folderSettings
    
    ns.addIfDifferent(  st.FOLDERS_SETTINGS_ESTIMATE,   fds.estimateDates,        FDS.D_ESTIMATE_DATES)
    ns.addIfDifferent(st.USE, fds.use, FDS.D_USE)
    
    
    folderSettingsNode = OrderedNode(st.FOLDERS_SETTINGS_NODE, ns)
        
    if (not folderSettingsNode.hasSettings()):
        return None
    
    return folderSettingsNode