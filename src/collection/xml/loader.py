import strings as st
from src.collection.Collection import Collection, D_TITLE, D_THUMB, D_DEFAULT
import src.collection.settings.FeedSettings as fs
import src.collection.settings.FeedTextSettings as fTS
import src.collection.settings.SourcesSettings as ss
import src.collection.settings.SourcesTextSettings as sTS
import src.collection.settings.FolderSettings as fds
from src.videosource.youtube import Channel
from src.videosource.youtube import Playlist
from src.videosource.youtube import batchUpdater
from src.videosource.kodi import KodiFolder
import src.cxml.loader as cxml
from src.li.visual.TextSettings import TextSettings
from src.cxml import Node
from src.collection.csource import KodiCollectionSource



#COLLECTION_DIC_FILE = '__collections.dic'



# def load(collectionFile):
#     dicFile = File.fromNameAndDir(COLLECTION_DIC_FILE, COLLECTIONS_CACHE_DIR)
#     if dicFile.exists():
#         collectionDic = dicFile.loadObject()                    
#         xmlFP = collectionFile.fullpath
#                     
#         if xmlFP in collectionDic:                      #check if this collection was ever cached
#             dumpFileFP = collectionDic[xmlFP]
#             dumpFile = File.fromFullpath(dumpFileFP)
#                         
#             collection = dumpFile.loadObject()
#             
#             if collection.cachedXml == collectionFile.contents():  #xml is same, we can use the data from before
#                 collection.refetchInfoIfTime()                       #unless a long time passed. if so, refetch it
#                 return collection                                  
#             
#             else:                                               #xml changed so we reload and redump the collection
#                 collection = _load(collectionFile, dumpFile)    #dic doesn't need to be touched
#                 return collection 
#      
#     else:
#         collectionDic = {}
#              
#              
#     
#                                                         
#     collection = _load(collectionFile)                                      #either there was no dic file at all, or collection
#                                                                             #was never cached. we load the collection from 
#     collectionDic[collectionFile.fullpath] = collection.dumpFile.fullpath   #scratch, find a new available dump file and dump it.
#     dicFile.dumpObject(collectionDic)                                       #we also add it to the dic and dump/redump the dic
#                                                              
#     return collection


    
    
    
    
#def _load(collectionFile, dumpFile=None):
#     if dumpFile is None:
#         name = collectionFile.soleName + '.col'
#         dumpFile = File.fromNameAndDir(name, COLLECTIONS_CACHE_DIR)    
#         while dumpFile.exists():
#             dumpFile =  File.fromFullpath (dumpFile.path + '/' + dumpFile.soleName + '_' + '.col')


def loadSources(collection):
    root  = cxml.load(collection.file)
    sourcesNodes = _processNodes(root.children)[0]
    _processSources(sourcesNodes, collection)
    
    

ranInit = False

def load(collectionFile, loadSources=True, isGlobal=False):
    root  = cxml.load(collectionFile)
    sourcesNodes, settingsNodes = _processNodes(root.children)
    
    title, onClick, default = _processRoot(root)          
    fs, ss, fds = _processSettings(settingsNodes)
    thumb = _processThumb(collectionFile)
    
    
    collection = Collection(title, thumb, fs, ss, fds, collectionFile, default, onClick)
    
        
    if loadSources: 
        _processSources(sourcesNodes, collection)
                                    
                    
                        


    

    
    #no sure bout this being here, or if it's written precisely, but seems to be working
    if (not isGlobal) and (not ranInit):
        _runInit()

    
    return collection
                
                
            
            
            
    #collection.fetchInfo()
    #collection.updateVideoList()        #not sure
    #collection.dump()
    
    
    #
    

    

def _processRoot(root):
    #get collection settings and set defaults if not specified
    title = root.text if root.text else D_TITLE
    
    s = root.settings        
    onClick =     _get(s,     st.ON_CLICK,    st.valueToOcc)
    default =     s.get(      st.COLLECTION_DEFAULT,          D_DEFAULT)

    return title, onClick, default


def _processNodes(nodes):    
    viewsIndex = None
    
    index = 0
    for node in nodes:
        if node.name == st.VIEWS_NODE:
            viewsIndex = index
            break
                    
        index += 1
    
    if viewsIndex is not None:     
        sourcesNodes  = nodes [:viewsIndex]
        settingsNodes = nodes [viewsIndex+1:]
    else:
        sourcesNodes = nodes
        settingsNodes = ();
        
    return sourcesNodes, settingsNodes





def _processSettings(settingsNodes):
    feedSettings = None
    sourcesSettings = None
    folderSettings = None
    
    
    for node in settingsNodes:        
        if node.name == st.FEED_NODE:
            feedSettings = _processFeedSettings(node)
        elif node.name == st.SOURCES_NODE: 
            sourcesSettings = _processSourcesSettings(node)
        else:
            folderSettings = _processFolderSettings(node)

    feedSettings    = feedSettings if feedSettings          else _processFeedSettings(      Node.empty(st.FEED_NODE))         
    sourcesSettings = sourcesSettings if sourcesSettings    else _processSourcesSettings(   Node.empty(st.SOURCES_NODE))
    folderSettings  = folderSettings if folderSettings      else _processFolderSettings(    Node.empty(st.FOLDERS_SETTINGS_NODE))


    return feedSettings, sourcesSettings, folderSettings







def _processSources(sourcesNodes, collection):
    cSourceItems = []
    ytSourcesToUpdate = []
    
    for node in sourcesNodes:
        for textRow in node.textRows:            
            onSourceClick, limit, customTitle, customThumb = _processCSourceSettings(textRow.settings)
            
            if node.name == st.FOLDERS_NODE:
                vSource, estimateDates = _processFolder(textRow, customTitle, customThumb)
                
                                
            else:
                if node.name == st.CHANNELS_NODE:                                  
                    vSource, needsInfoUpdate = _processChannel(textRow)
                else:
                    vSource, needsInfoUpdate = _processPlaylist(textRow)
                    
                estimateDates = None
                                     
                if needsInfoUpdate:
                    ytSourcesToUpdate.append(vSource)
                
                
            
            cSourceItems.append((vSource, onSourceClick, limit, customTitle, customThumb, estimateDates))    
                        
                        
    batchUpdater.infoUpdate(ytSourcesToUpdate, forceUpdate=True)

    for cSourceItem in cSourceItems:
        videoSource, onSourceClick, limit, customTitle, customThumb, estimateDates = cSourceItem
        collection.addCollectionSource(videoSource, onSourceClick, limit, customTitle, customThumb, estimateDates)
        
    collection.setLoadedSources()






def _processThumb(collectionFile):
    thumb = D_THUMB
    
    cFolder = collectionFile.folder
    if cFolder.hasSubfolder('_images'):
        imageFolder = cFolder.getSubfolder('_images')
        soleName = collectionFile.soleName
            
        if imageFolder.hasFile(soleName + '.png'):
            thumb = imageFolder.getFile(soleName + '.png').fullpath
            
        elif imageFolder.hasFile(soleName + '.jpg'):
            thumb = imageFolder.getFile(soleName + '.jpg').fullpath
            
                
    return thumb       





def _processCSourceSettings(textrowSettings):    
    onClick     =   _get(textrowSettings,   st.ON_CLICK,                st.valueToOsc)        
    limit       =   textrowSettings.get(    st.CSOURCE_LIMIT)                        
    customTitle =   textrowSettings.get(    st.CSOURCE_CUSTOM_TITLE)
    customThumb =   textrowSettings.get(    st.CSOURCE_CUSTOM_THUMB)
    
    if limit and limit > fs.MAX_LIMIT:
        limit = fs.MAX_LIMIT
        
                    
    return onClick, limit, customTitle, customThumb
        


def _processChannel(textrow):        
    settings = textrow.settings
    
    if settings.get(st.CHANNEL_ID):
        channelId = textrow.text
        username = None
    else:
        username = textrow.text
        channelId = None
    
    
    channel, needsInfoUpdate = Channel.fromUserOrId(channelId, username)
    return channel, needsInfoUpdate
            




def _processPlaylist(textrow):    
    playlistId = textrow.text       
              
    playlist, needsInfoUpdate = Playlist.fromPlaylistId(playlistId)    
    return playlist, needsInfoUpdate






def _processFolder(textrow, customTitle, customThumb):    
    path = textrow.text    
    settings = textrow.settings
    estimateDates = settings.get(st.FOLDER_ESTIMATE_DATES)
    
    title = customTitle   #we give it same title and thumb as custom title and thumb, which are the original listed title
    thumb = customThumb   #and thumb if unchanged by the user later. best solution i can currently think of for now.
                                            
        
    kodiFolder = KodiFolder.fromPath(path, title, thumb)
        
    return kodiFolder, estimateDates








def _processTS(textRowSettings, default, returnSeperated=False):
    s = textRowSettings
    
    color   = s.get( st.TS_COLOR,   default.color)
    bold    = s.get( st.TS_BOLD,    default.bold)
    italic  = s.get( st.TS_ITALIC,  default.italic)
    show    = s.get( st.TS_SHOW,    default.show)
    
    if returnSeperated:
        return color, bold, italic, show
    
    return TextSettings(color, bold, italic, show)


# def _processCTS(textRowSettings, default):
#     s = textRowSettings
#      
#     ts = _processTS (s, default)
#     location   = _get(s,    st.CTS_LOACTION,  st.valueToLoc,        default.location)
#      
#     return ts, location 
    
     


def _processFeedSettings(feedNode):
    ns = feedNode.settings
    viewStyle   =   ns.get(     st.VIEWSTYLE,                           fs.D_VIEWSTYLE)
    videoSort   =   _get(ns,    st.FEED_SORT,       st.valueTovsr,      fs.D_SORT)
    videoSort2  =   _get(ns,    st.FEED_SORT2,      st.valueTovsr,      fs.D_SORT2,         nonePossible=True)
    revSort     =   ns.get(     st.FEED_REVSORT,                        fs.D_REVERSE_SORT)
    countType   =   _get(ns,    st.FEED_COUNT_TYPE, st.valueToVct,      fs.D_COUNT_TYPE)
    countType2  =   _get(ns,    st.FEED_COUNT_TYPE2,st.valueToVct,      fs.D_COUNT_TYPE2,   nonePossible=True)   
    #repViews    =   ns.get(     st.FEED_REPVIEWS,                       fs.D_REPLACE_VIEWS)
    onVideoClick=   _get(ns,    st.FEED_VIDEOCLICK, st.valueToOvc,      fs.D_VIDEOCLICK)               
    unwatched   =   ns.get(     st.FEED_UNWATCHED,                      fs.D_UNWATCHED)
    limit       =   ns.get(     st.FEED_LIMIT,                          fs.D_LIMIT)
    sLimit      =   ns.get(     st.FEED_SLIMIT,                         fs.D_SLIMIT)
    
    use =           ns.get(st.USE,          fs.D_USE)
    useLimits =     ns.get(st.USELIMITS,    fs.D_USELIMITS)
    useTS =         ns.get(st.USETS,        fTS.D_USE)
    
    
    countLoc    =   _get(ns,    st.COUNT_LOACTION,  st.valueToLoc,      fTS.D_COUNT_LOCATION)
    
    
    
    browseSourcesTS =   fTS.D_BROWSE_SOURCES
    settingsTS      =   fTS.D_SETTINGS
    sortTS          =   fTS.D_SORT
    playAllTS       =   fTS.D_PLAY_ALL
        
    countTS         =   fTS.D_COUNT
    count2TS        =   fTS.D_COUNT2    
    videoSource     =   fTS.D_VIDEO_SOURCE
    videoTitle      =   fTS.D_VIDEO_TITLE
    
    for textRow in feedNode.textRows:
        if textRow.text == st.FEED_TR_BROWSE_SOURCES:   browseSourcesTS =   _processTS(textRow.settings,    fTS.D_BROWSE_SOURCES)
        if textRow.text == st.FEED_TR_SETTINGS:         settingsTS      =   _processTS(textRow.settings,    fTS.D_SETTINGS)
        if textRow.text == st.FEED_TR_SORT:             sortTS          =   _processTS(textRow.settings,    fTS.D_SORT)
        if textRow.text == st.FEED_TR_PLAYALL:          playAllTS       =   _processTS(textRow.settings,    fTS.D_PLAY_ALL)
        
        if textRow.text == st.FEED_TR_VIDEO_COUNT:      countTS         =   _processTS(textRow.settings,   fTS.D_COUNT)
        if textRow.text == st.FEED_TR_VIDEO_COUNT2:     count2TS        =   _processTS(textRow.settings,    fTS.D_COUNT2)
        if textRow.text == st.FEED_TR_VIDEO_SOURCE:     videoSource     =   _processTS(textRow.settings,    fTS.D_VIDEO_SOURCE)
        if textRow.text == st.FEED_TR_VIDEO_TITLE:      videoTitle      =   _processTS(textRow.settings,    fTS.D_VIDEO_TITLE)
        
        
        
    feedTS = fTS.fromSeperated(browseSourcesTS, settingsTS, sortTS, playAllTS,  countTS, count2TS, 
                               countLoc, videoSource, videoTitle, useTS)
    
    feedSettings = fs.FeedSettings(viewStyle, videoSort, videoSort2, revSort, countType, countType2, onVideoClick, unwatched, limit, sLimit, use, useLimits, feedTS)    
    return feedSettings 
    
    
        
def _processSourcesSettings(sourcesNode):
    ns = sourcesNode.settings
    viewStyle           =   ns.get(     st.VIEWSTYLE,                                           ss.D_VIEWSTYLE)
    onSourceClickKodi   =   _get(ns,    st.SOURCES_SOURCE_CLICK_KODI,  st.valueToOsc,           ss.D_SOURCE_CLICK_KODI)
    onSourceClickYt     =   _get(ns,    st.SOURCES_SOURCE_CLICK_YT,    st.valueToOsc,           ss.D_SOURCE_CLICK_YT)
    
    
    use                 =   ns.get( st.USE,     ss.D_USE)
    useTS               =   ns.get( st.USETS,   sTS.D_USE)
    
    
     
    
    
    
    cSourceTS = sTS.D_CSOURCE
    
    for textRow in sourcesNode.textRows:
        if textRow.text == st.SOURCES_TR_CSOURCE: cSourceTS =   _processTS(textRow.settings,    sTS.D_CSOURCE)
        
    sourcesTS = sTS.SourcesTextSettings(cSourceTS, useTS)
    
    sourcesSettings = ss.SourcesSettings(viewStyle, onSourceClickKodi, onSourceClickYt, use, sourcesTS)
    return sourcesSettings



def _processFolderSettings(folderSettingsNode):
    ns = folderSettingsNode.settings        
    estimateDates   = ns.get(st.FOLDERS_SETTINGS_ESTIMATE,  fds.D_ESTIMATE_DATES)    
    use             = ns.get(st.USE,                        fds.D_USE)
    
    
    folderSettings = fds.FolderSettings(estimateDates, use)
    return folderSettings






def _runInit():   
    from src.collection import Collection as c
    from src.collection import CollectionSource as cs
    from src.collection.csource import YoutubeCollectionSource
    
    
    c.init()
    cs.init()
    KodiCollectionSource.init()
    YoutubeCollectionSource.init()
    
    fs.init()
    fTS.init()
    ss.init()
    sTS.init()
    fds.init()
    
    global ranInit
    ranInit = True





def _get (dic, key, conversionDic, default=None, nonePossible=False):
    if not key in dic:
        return default

    else:
        value = dic[key]
        if (nonePossible) and (value is None):
            return None
        
        return conversionDic[value]