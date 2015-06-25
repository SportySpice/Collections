import strings as st
import src.collection.Collection as c
from src.collection.settings import FeedSettings as FS
from src.collection.settings import FeedTextSettings as FTS
from src.collection.settings import SourcesSettings as SS
from src.collection.settings import SourcesTextSettings as STS
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
        nodeName, textRow =  options[vSource.type](vSource, s)
        
        s.addIfNotNone( st.ON_CLICK,                cSource._onClick,       customValueDic=st.oscToValue)                    
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
                    
    
    feedNode    =   _processFeedSettings(collection)
    sourcesNode =   _processSourcesSettings(collection) 
    
    if feedNode or sourcesNode:
        views = OrderedNode(st.VIEWS_NODE)        
        if feedNode:    views.addChild(feedNode)
        if sourcesNode: views.addChild(sourcesNode)
        
        nodeList.append(views)
    
    
    rootNode.addChildren(nodeList)
    xmlExporter.export(rootNode, collection.file)
                    
                 
                 
                 
                 
                 
                    
def _processChannel(channel, sourceSettings):
    if channel.username:
        text = channel.username
        comment = None
        
    else:
        text = channel.channelId
        sourceSettings.add(st.CHANNEL_ID, True)
        comment = channel.title
    
    return st.CHANNELS_NODE, OrderedTextRow(text, sourceSettings, comment=comment)



def _processPlaylist(playlist, sourceSettings):
    text = playlist.playlistId   
    comment =  playlist.title
    
    return st.PLAYLISTS_NODE, OrderedTextRow(text, sourceSettings, comment=comment)



def _processKodiFolder(folder, sourceSettings):
    text = folder.path
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
        
    


def _processCTS(name, CTS, defaultCTS):
    s = _processTS(name, CTS, defaultCTS, returnSettings=True)
    
    s.addIfDifferent(   st.CTS_LOACTION,    CTS.location,   defaultCTS.location,        customValueDic=st.locToValue)
    s.addIfDifferent(   st.CTS_TYPE,        CTS.countType,  defaultCTS.countType,       customValueDic=st.ctToValue)


    if not s.hasValues():
        return None
    
    return OrderedTextRow(name, s)




def _processFeedSettings(collection):
    ns = OrderedSettings()
    fs = collection.feedSettings
    fts = fs.TS
    videoFTS = fts._videoFTS
    
    ns.addIfDifferent(  st.VIEWSTYLE,       fs._viewStyle,      FS.D_VIEWSTYLE)
    ns.addIfDifferent(  st.FEED_VIDEOCLICK, fs._onVideoClick,   FS.D_VIDEOCLICK,        customValueDic=st.ovcToValue)
    ns.addIfDifferent(  st.FEED_UNWATCHED,  fs._unwatched,      FS.D_UNWATCHED)
    ns.addIfDifferent(  st.FEED_LIMIT,      fs._limit,          FS.D_LIMIT)
    ns.addIfDifferent(  st.FEED_SLIMIT,     fs.sLimit,          FS.D_SLIMIT)
    
    ns.addIfDifferent(  st.USE,             fs.use,              FS.D_USE)
    ns.addIfDifferent(  st.USETS,           fts.use,            FTS.D_USE)
    
    browseSourcesTR =   _processTS( st.FEED_TR_BROWSE_SOURCES,  fts._browseSourcesTS,   FTS.D_BROWSE_SOURCES    )
    settingsTR      =   _processTS( st.FEED_TR_SETTINGS,        fts._settingsTS,        FTS.D_SETTINGS          )
    playAllTR       =   _processTS( st.FEED_TR_PLAYALL,         fts._playAllTS,         FTS.D_PLAY_ALL          )
        
    videoCountTR    =   _processCTS(st.FEED_TR_VIDEO_COUNT,     videoFTS.countTS,       FTS.D_VIDEO_COUNT       )
    videoSourceTR   =   _processTS( st.FEED_TR_VIDEO_SOURCE,    videoFTS.sourceTS,      FTS.D_VIDEO_SOURCE      )
    videoTitleTR    =   _processTS( st.FEED_TR_VIDEO_TITLE,     videoFTS.titleTS,       FTS.D_VIDEO_TITLE       )
    
    
    feedNode = OrderedNode(st.FEED_NODE, ns)
    
    if browseSourcesTR: feedNode.addTextRow(browseSourcesTR)
    if settingsTR:      feedNode.addTextRow(settingsTR)
    if playAllTR:       feedNode.addTextRow(playAllTR)
    
    if videoCountTR:    feedNode.addTextRow(videoCountTR)
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