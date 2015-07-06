import urllib
import urlparse

# from tools import debug
# debug.start()


ROOT                    =       'plugin://plugin.video.collections/'
#HOME                   =        ?
PLAY_VIDEO_KODI         =       'plugin://plugin.video.collections/play/video/kodi'
PLAY_VIDEO_YOUTUBE      =       'plugin://plugin.video.collections/play/video/youtube'
PLAY_QUEUE_PLAYLIST     =       'plugin://plugin.video.collections/play/queue/playlist'
PLAY_QUEUE_COLLECTION   =       'plugin://plugin.video.collections/play/queue/collection'
PLAY_COLLECTION         =       'plugin://plugin.video.collections/play/collection'


BROWSE_FOLDER           =       'plugin://plugin.video.collections/browse/folder'
BROWSE_COLLECTION       =       'plugin://plugin.video.collections/browse/collection'
BROWSE_CSOURCES         =       'plugin://plugin.video.collections/browse/collection/sources'
BROWSE_FOR_SOURCES      =       'plugin://plugin.video.collections/browse/newsources'
BROWSE_KODI_FOLDER      =       'plugin://plugin.video.collections/browse/kodi/folder'
BROWSE_YT_CHANNEL       =       'plugin://plugin.video.collections/browse/youtube/channel'
BROWSE_YT_CHANNEL_PLS   =       'plugin://plugin.video.collections/browse/youtube/channel/playlists'
BROWSE_YT_PLAYLIST      =       'plugin://plugin.video.collections/browse/youtube/playlist'
BROWSE_YT_SUBSCRIPTIONS =       'plugin://plugin.video.collections/browse/youtube/subscriptions'
BROWSE_YT_CATEGORIES    =       'plugin://plugin.video.collections/browse/youtube/categories'
BROWSE_YT_CATEGORY      =       'plugin://plugin.video.collections/browse/youtube/category'
BROWSE_LOCAL_STORAGE    =       'plugin://plugin.video.collections/browse/local/storage'

SEARCH_YOUTUBE_SELECT   =       'plugin://plugin.video.collections/search/youtube/select'
SEARCH_YOUTUBE          =       'plugin://plugin.video.collections/search/youtube'

ADD_TO_COLLECTION       =       'plugin://plugin.video.collections/add/source'
ADD_TO_COLLECTION_BROWSE=       'plugin://plugin.video.collections/add/source/brows'
REMOVE_FROM_COLLECTION  =       'plugin://plugin.video.collections/remove/source'
DELETE_COLLECTION       =       'plugin://plugin.video.collections/delete/collection'

SIGN_IN_OUT_YOUTBE      =       'plugin://plugin.video.collections/sign/youtube'

EDIT_COLLECTION         =       'plugin://plugin.video.collections/edit/collection'
EDIT_KODI_FOLDER        =       'plugin://plugin.video.collections/edit/kodi/folder'
EDIT_YT_CHANNEL         =       'plugin://plugin.video.collections/edit/youtube/channel'
EDIT_YT_CHANNEL_PLS     =       'plugin://plugin.video.collections/edit/youtube/channel/playlists'
EDIT_YT_PLAYLIST        =       'plugin://plugin.video.collections/edit/youtube/playlist'
EDIT_YT_SUBSCRIPTIONS   =       'plugin://plugin.video.collections/edit/youtube/subscriptions'
EDIT_YT_SEARCH          =       'plugin://plugin.video.collections/edit/youtube/search'
EDIT_YT_CATEGORY        =       'plugin://plugin.video.collections/edit/youtube/subscriptions'

SORT_VIDEOLIST          =       'plugin://plugin.video.collections/sort/videolist'

DELETE_CACHE            =       'plugin://plugin.video.collections/delete/cache'






def rootUrl():
    return ROOT

def root(query):
    from src.paths import root
    root.root()
#     from src.paths import plugin_test
#     plugin_test.test()


# def homeUrl():
#     return HOME
# 
# def home(query):
#     from src.paths import home
#     home.home()




def playVideoKodiUrl(path):
    return _encodedUrlSingle(PLAY_VIDEO_KODI, path)

def playVideoKodi(query):
    from paths import play_video_kodi
    
    path = _decodedUrlSingle(query)
    play_video_kodi.play(path)


def playVideoYoutubeUrl(videoId):
    return _simpleUrl(PLAY_VIDEO_YOUTUBE, videoId)
    
def playVideoYoutube(query):
    from paths import play_video_youtube
    
    videoId = query
    play_video_youtube.play(videoId)
    
    



def playQueueCollectionUrl(videoId, collectionFile):
    return _joinedUrl(PLAY_QUEUE_COLLECTION, (videoId, collectionFile.encodedQuery()))
    
def playQueueCollection(query):
    from file import File
    from paths import play_queue_collection
    
    
    videoId, collectionFile = _unjoinedQuery(query)
    collectionFile = File.fromQuery(collectionFile)
    play_queue_collection.play(videoId, collectionFile)
    
    
    
    
def playCollectionUrl(collectionFile):
    return _simpleUrl(PLAY_COLLECTION, collectionFile.encodedQuery())

def playCollection(query):
    from file import File
    from paths import play_collection
        
    collectionFile = File.fromQuery(query)
    play_collection.play(collectionFile)
    
    


def browseFolderUrl(folder):
    return _simpleUrl(BROWSE_FOLDER, folder.encodedQuery())

def browseFolder(query):
    from file import Folder
    from paths import browse_folder
    
    folder = Folder.fromQuery(query)
    browse_folder.browse(folder)    
    
    
    
    
def browseCollectionUrl(collectionFile):
    return _simpleUrl(BROWSE_COLLECTION, collectionFile.encodedQuery())
    
def browseCollection(query):
    from file import File
    from paths import browse_collection
        
    collectionFile = File.fromQuery(query)
    browse_collection.present(collectionFile)
    
    
    
def browseCollectionSourcesUrl(collectionFile):
    return _simpleUrl(BROWSE_CSOURCES, collectionFile.encodedQuery())

def browseCollectionSources(query):
    from file import File
    from paths import browse_collection_sources
    
    collectionFile = File.fromQuery(query)
    browse_collection_sources.browse(collectionFile)




def browseForSourcesUrl():
    return BROWSE_FOR_SOURCES


def browseForSources(query):
    from paths import browse_for_sources
    browse_for_sources.browse()
    
    
    
def browseKodiFolderUrl(kodiFolderFile, root=False):
    return _encodedUrl(BROWSE_KODI_FOLDER, (kodiFolderFile.fullpath, root))

def browseKodiFolder(query):
    from paths import browse_kodi_folder
    from file import File
    
    kodiFolderFile, root = _decodedUrl(query)
    kodiFolderFile = File.fromFullpath(kodiFolderFile)
    
    browse_kodi_folder.browse(kodiFolderFile, root)
    
    
    
def browseYoutubeCategoriesUrl():
    return BROWSE_YT_CATEGORIES

def browseYoutubeCategories(query):
    from paths import browse_youtube_categories
    browse_youtube_categories.browse()
    
    
    
    
    
def browseYoutubeCategoryUrl(categoryFile, pageNum=1):
    return _encodedUrl(BROWSE_YT_CATEGORY, (categoryFile.fullpath, pageNum))

def browseYoutubeCategory(query):
    from paths import browse_youtube_category
    from file import File
    
    categoryFile, pageNum = _decodedUrl(query)
    categoryFile = File.fromFullpath(categoryFile)
    
    browse_youtube_category.browse(categoryFile, pageNum)
    
    
    
    
    
    
def browseYoutubeChannelUrl(channelFile, pageNum=1):
    return _encodedUrl(BROWSE_YT_CHANNEL, (channelFile.fullpath, pageNum))

def browseYoutubeChannel(query):
    from paths import browse_youtube_channel
    from src.file import File
    
    channelFile, pageNum = _decodedUrl(query)
    channelFile = File.fromFullpath(channelFile)
    
    browse_youtube_channel.browse(channelFile, pageNum)
    
    
    
def browseYoutubeChannelPlaylistsUrl(channelFile, pageNum=1):
    return _encodedUrl(BROWSE_YT_CHANNEL_PLS, (channelFile.fullpath, pageNum))
    
    
def browseYoutubeChannelPlaylists(query):
    from paths import browse_youtube_channel_playlists
    from src.file import File
    
    channelFile, pageNum = _decodedUrl(query)
    channelFile = File.fromFullpath(channelFile)
    
    browse_youtube_channel_playlists.browse(channelFile, pageNum)



def browseYoutubePlaylistUrl(playlistFile, pageNum=1):
    return _encodedUrl(BROWSE_YT_PLAYLIST, (playlistFile.fullpath, pageNum))

def browseYoutubePlaylist(query):
    from paths import browse_youtube_playlist
    from src.file import File
    
    playlistFile, pageNum = _decodedUrl(query)
    playlistFile = File.fromFullpath(playlistFile)
    
    browse_youtube_playlist.browse(playlistFile, pageNum)



def searchYoutubeSelectUrl():
    return SEARCH_YOUTUBE_SELECT

def searchYoutubeSelect(query):
    from src.paths import search_youtube_select
    search_youtube_select.select()




def searchYoutubedUrl(searchType=None, searchFile=None, pageNum=1):
    if searchFile:
        searchFile = searchFile.fullpath
    return _encodedUrl(SEARCH_YOUTUBE, (searchType, searchFile, pageNum))

def searchYoutube(query):
    from paths import search_youtube
    from src.file import File
    
    searchType, searchFile, pageNum = _decodedUrl(query)
    if searchFile:
        searchFile = File.fromFullpath(searchFile)
    search_youtube.search(searchType, searchFile, pageNum)
    
    
    
def browseYoutubeSubscriptionsUrl(pageNum=1):
    return _simpleUrl(BROWSE_YT_SUBSCRIPTIONS, pageNum)

def browseYoutubeSubscriptions(query):
    from paths import browse_youtube_subscriptions
    
    pageNum = _unsimpledQuery(query)
    browse_youtube_subscriptions.browse(pageNum)
    

def addToCollectionUrl(vSourceId, vSourceFile, sourceType):
    return _encodedUrl(ADD_TO_COLLECTION, (vSourceId, vSourceFile.fullpath, sourceType))

def addToCollection(query):
    from paths import add_to_collection
    from src.file import File
    
    vSourceId, vSourceFile, sourceType = _decodedUrl(query)
    vSourceFile = File.fromFullpath(vSourceFile)
    add_to_collection.add(vSourceId, vSourceFile, sourceType)
    
    
def addToCollectionBrowseUrl(relativePath=''):
    if relativePath:
        return ADD_TO_COLLECTION_BROWSE + relativePath
     
    return ADD_TO_COLLECTION_BROWSE
      

def addToCollectionBrowse(path):
    from paths import add_to_collection_browse
    
    baseLength = len(ADD_TO_COLLECTION_BROWSE)
    relativePath = path[baseLength:]
     
    
    add_to_collection_browse.browse(relativePath)


def removeFromCollectionUrl(collectionFile, sourceId, showConfirmDialog=True, showSuccessDialog=True, refreshContainer=True):
    return _encodedUrl(REMOVE_FROM_COLLECTION, [collectionFile.fullpath, sourceId, showConfirmDialog, showSuccessDialog, refreshContainer])

def removeFromCollection(query):
    from paths import remove_from_collection
    from src.file import File
    
    collectionFile, sourceId, showConfirmDialog, showSuccessDialog, refreshContainer = _decodedUrl(query)
    collectionFile = File.fromFullpath(collectionFile) 
       
    remove_from_collection.remove(collectionFile, sourceId, showConfirmDialog, showSuccessDialog, refreshContainer)

    
def signInOutYoutubeUrl():
    return SIGN_IN_OUT_YOUTBE

def signInOutYoutube(query):
    from paths import sign_in_out_youtube
    sign_in_out_youtube.sign()
    

def deleteCacheUrl():
    return DELETE_CACHE

def deleteCache(query):
    from paths import delete_cache
    delete_cache.delete()


    
    
    
def browseLocalStorageUrl():
    return BROWSE_LOCAL_STORAGE

def browseLocalStorage(query):
    from paths import browse_local_storage
    browse_local_storage.browse()
    


def deleteCollectionUrl(collectionFile, showConfirmDialog=True, showSuccessDialog=True, refreshContainer=True):
    return _encodedUrl(DELETE_COLLECTION, [collectionFile.fullpath, showConfirmDialog, showSuccessDialog, refreshContainer])

def deleteCollection(query):
    from paths import delete_collection
    from src.file import File
    
    collectionFile, showConfirmDialog, showSuccessDialog, refreshContainer = _decodedUrl(query)
    collectionFile = File.fromFullpath(collectionFile) 
       
    delete_collection.delete(collectionFile, showConfirmDialog, showSuccessDialog, refreshContainer)




def editCollectionUrl(collectionFile=None):
    if not collectionFile:
        return EDIT_COLLECTION
    
    return _simpleUrl(EDIT_COLLECTION, collectionFile.encodedQuery())

def editCollection(query):
    from src.paths import edit_collection
    from src.file import File
    
    collectionFile = _unsimpledQuery(query)
    if collectionFile:
        collectionFile = File.fromQuery(query)
        
    edit_collection.edit(collectionFile)
    
def sortVideolistUrl(sourceType=None):
    return _simpleUrl(SORT_VIDEOLIST, sourceType)

def sortVideolist(query):
    from src.paths import sort_videolist
    
    sourceType = _unsimpledQuery(query)
    sort_videolist.sort(sourceType)
    
    
def editKodiFolderUrl():
    return EDIT_KODI_FOLDER

def editKodiFolder(query):
    pass


def editYtSubscriptionsUrl():
    return EDIT_YT_SUBSCRIPTIONS


def editYtSubscriptions(query):
    from src.paths import edit_youtube_subscriptions
    edit_youtube_subscriptions.edit()
    

def editTemp(query):
    from src.tools.dialog import dialog
    dialog.ok('Soon', 'Coming Soon!')
    

def playQueuePlaylistUrl(videoIndex=0):
    return _simpleUrl(PLAY_QUEUE_PLAYLIST, videoIndex)

def playQueuePlaylist(query):
    from src.paths import play_playlist
    
    videoIndex = _unsimpledQuery(query)
    play_playlist.play(videoIndex)




def route(path, query):    
    if path.startswith(ADD_TO_COLLECTION_BROWSE):
        addToCollectionBrowse(path)
    
    
    else:
        pathes = {ROOT:root, PLAY_VIDEO_KODI:playVideoKodi, PLAY_VIDEO_YOUTUBE:playVideoYoutube,
                  PLAY_QUEUE_COLLECTION:playQueueCollection,
                  PLAY_COLLECTION:playCollection, BROWSE_FOLDER:browseFolder, BROWSE_COLLECTION:browseCollection,
                  BROWSE_CSOURCES:browseCollectionSources, BROWSE_FOR_SOURCES:browseForSources,
                  BROWSE_KODI_FOLDER:browseKodiFolder, BROWSE_YT_CATEGORIES:browseYoutubeCategories,
                  BROWSE_YT_CATEGORY:browseYoutubeCategory, BROWSE_YT_CHANNEL:browseYoutubeChannel,
                  BROWSE_YT_CHANNEL_PLS:browseYoutubeChannelPlaylists, BROWSE_YT_PLAYLIST:browseYoutubePlaylist,
                  SEARCH_YOUTUBE_SELECT:searchYoutubeSelect, SEARCH_YOUTUBE:searchYoutube,
                  BROWSE_YT_SUBSCRIPTIONS:browseYoutubeSubscriptions, ADD_TO_COLLECTION:addToCollection,
                  SIGN_IN_OUT_YOUTBE:signInOutYoutube, DELETE_CACHE:deleteCache, 
                  EDIT_COLLECTION:editCollection, REMOVE_FROM_COLLECTION:removeFromCollection,
                  BROWSE_LOCAL_STORAGE:browseLocalStorage, DELETE_COLLECTION:deleteCollection, 
                  EDIT_KODI_FOLDER:editTemp, EDIT_YT_CHANNEL:editTemp, 
                  EDIT_YT_CHANNEL_PLS:editTemp, EDIT_YT_PLAYLIST:editTemp,
                  EDIT_YT_SUBSCRIPTIONS:editTemp, EDIT_YT_SEARCH:editTemp, 
                  EDIT_YT_CATEGORY:editTemp, SORT_VIDEOLIST:sortVideolist, 
                  PLAY_QUEUE_PLAYLIST:playQueuePlaylist}
         
        pathes[path](query)
   
 
    
    
    
    
    



def _simpleUrl(path, query):
    if query == None:
        return path
    
    if type(query) == int:
        query = str(query)
    return path + '?' + query

def _unsimpledQuery(query):
    if query == '':
        return None
    
    if query.isdigit():
        query = int(query)
        
    return query




SEPERATOR = '%2c%2c%2c'

def _joinedUrl(path, stringList):
    query = stringList[0]
    
    for i in range(1, len(stringList)):
        string = stringList[i]
        query += SEPERATOR + string
        
    return path + '?' + query
    
    
def _unjoinedQuery(query):
    stringList = query.split(SEPERATOR)            
    return stringList
        





 
def _encodedUrlSingle(path, string):
    params = {'string':string}
    query = urllib.urlencode(params)
    
    return path + '?' + query

def _decodedUrlSingle(query):
    parsedQuery = urlparse.parse_qs(query)
    string = parsedQuery['string'][0]
    
    return string 



def _encodedUrl(path, itemList):
    #params = {'stringList': stringList}
    #query = urllib.urlencode(params, true)
    dic = {}
    index = 0
    for item in itemList:
        dic[index] = item
        index += 1
    query = urllib.urlencode(dic)
    
 
    return path + '?' + query

         
def _decodedUrl(query):
    tuples = urlparse.parse_qsl(query)
    itemList = []
    for _tuple in tuples:
        item = _tuple[1]
        if item=='None':
            item = None
        elif item=='True':
            item =  True
        elif item=='False':
            item = False
        elif item.isdigit():
            item = int(item)
            
            
            
        itemList.append(item)
    
     
    return itemList
    
    


# def _encodedUrl(path, dic):
#     query = urllib.urlencode(dic)    
#     return path + '?' + query
# 
# def _decodedQuery(query):
#     return urlparse.parse_qs(query)