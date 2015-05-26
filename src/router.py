ROOT                =       'plugin://plugin.video.collections/'
#HOME               =        ?
PLAY_VIDEO          =       'plugin://plugin.video.collections/play'
PLAY_VIDEO_SPECIAL  =       'plugin://plugin.video.collections/playspecial'
PLAY_VIDEO_SOURCE   =       'plugin://plugin.video.collections/playvideosource'
PLAY_COLLECTION     =       'plugin://plugin.video.collections/playall'
BROWSE_FOLDER       =       'plugin://plugin.video.collections/explore'
BROWSE_COLLECTION   =       'plugin://plugin.video.collections/collection'
BROWSE_SOURCE       =       'plugin://plugin.video.collections/source'
LIST_SOURCES        =       'plugin://plugin.video.collections/sourcelist'


def rootUrl():
    return ROOT

def root(query):
    from src.paths import root
    root.root()


# def homeUrl():
#     return HOME
# 
# def home(query):
#     from src.paths import home
#     home.home()





def playVideoUrl(videoId):
    return _simpleUrl(PLAY_VIDEO, videoId)
    
def playVideo(query):    
    from paths import play_video
    
    videoId = query
    play_video.play(videoId)
    
    
    
    
def playVideoSpecialUrl(videoId, collectionFile):
    return _encodedUrl(PLAY_VIDEO_SPECIAL, [videoId, collectionFile.encodedQuery()])
    
def playVideoSpecial(query):
    from file import File
    from paths import play_video_special
    
    
    videoId, collectionFile = _decodeQuery(query)
    collectionFile = File.fromQuery(collectionFile)
    play_video_special.play(videoId, collectionFile)
    
    
def playVideoSourceUrl(videoId, sourceId, collectionFile):
    return _encodedUrl(PLAY_VIDEO_SOURCE, [videoId, sourceId, collectionFile.encodedQuery()])
    
def playVideoSource(query):
    from file import File
    from paths import play_video_source
    
    videoId, sourceId, collectionFile = _decodeQuery(query)
    collectionFile = File.fromQuery(collectionFile)
    play_video_source.play(videoId, sourceId, collectionFile)
    
    
    
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
    browse_folder.explore(folder)    
    
    
    
    
def browseCollectionUrl(collectionFile):
    return _simpleUrl(BROWSE_COLLECTION, collectionFile.encodedQuery())
    
def browseCollection(query):
    from file import File
    from paths import browse_collection
        
    collectionFile = File.fromQuery(query)
    browse_collection.present(collectionFile)
    
    
    
def listSourcesUrl(collectionFile):
    return _simpleUrl(LIST_SOURCES, collectionFile.encodedQuery())

def listSources(query):
    from file import File
    from paths import list_sources
    
    collectionFile = File.fromQuery(query)
    list_sources.listSources(collectionFile)


    
def browseSourceUrl(sourceId, collectionFile):
    return _encodedUrl(BROWSE_SOURCE, [sourceId, collectionFile.encodedQuery()])
    
def browseSource(query):
    from file import File
    from paths import browse_source
    sourceId, collectionFile = _decodeQuery(query)
    collectionFile = File.fromQuery(collectionFile)
    
    browse_source.browse(sourceId, collectionFile)





def route(path, query):
#     from tools import debug
#     debug.start()
    
    pathes = {ROOT:root, PLAY_VIDEO:playVideo, PLAY_VIDEO_SPECIAL:playVideoSpecial,
              PLAY_VIDEO_SOURCE:playVideoSource, PLAY_COLLECTION:playCollection, 
              BROWSE_FOLDER:browseFolder, BROWSE_COLLECTION:browseCollection, 
              BROWSE_SOURCE:browseSource, LIST_SOURCES:listSources}
    
    pathes[path](query)
    
    
    
    
    
    
    



def _simpleUrl(path, query):
    return path + '?' + query




def _encodedUrl(path, stringList):
    query = stringList[0]
    
    for i in range(1, len(stringList)):
        string = stringList[i]
        query += '%2c%2c%2c' + string
        
    return path + '?' + query
    
def _decodeQuery(query):
    return query.split('%2c%2c%2c')