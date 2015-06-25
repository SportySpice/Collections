from Collection import Sort, Collection
from src.youtube.Channel import Channel
from src.youtube.Playlist import Playlist
from src.tools.xmlsoup import root, getAttrib, AttribType
from src.file import File
 
 
 
 
#############
## Defaults##
#############
DEFAULT_TITLE = 'No title'
DEFAULT_THUMB = 'special://home/addons/plugin.video.collections/icon.png'
DEFAULT_SORT = Sort.NEWEST
DEFAULT_COLLECTION_LIMIT = 50
DEFAULT_UNWATCHED = False
 
DEFAULT_GLOBAL_LIMIT = 20
DEFAULT_GLOBAL_REPEAT = 0
DEFAULT_GLOBAL_PUSH = 2
 
MAXLIMIT = 50   #google doesn't allow more than 50 items per request, will require multiple requests
 
##Unused options, might be added in future
#unwathced           #individual unwatched for every source, currently only works for entire collection
#subLimit            #limit a subcollection
#subRepeat           #configure maxrepeat of a subcollection
#subThumb            #thumb for the subcollection
#subTitle            #title for the subcollection
 
 
 
 
 
##########################
## Public Static Methods##
##########################
def load(fileQuery):
    collectionFile = File.fromQuery(fileQuery)
     
     
     
    #get collection settings and set defaults if not specified  
    xmlRoot,  = root(collectionFile)
    rootAttribs = xmlRoot.attrs                                       
    title =             getAttrib(rootAttribs, 'title',             DEFAULT_TITLE)
    thumb =             getAttrib(rootAttribs, 'thumb',             DEFAULT_THUMB)
    sort =              getAttrib(rootAttribs, 'sort',              DEFAULT_SORT)
    collectionLimit =   getAttrib(rootAttribs, 'collectionLimit',   DEFAULT_COLLECTION_LIMIT,   AttribType.INT)
    unwatched =         getAttrib(rootAttribs, 'unwatched',         DEFAULT_UNWATCHED,          AttribType.BOOL)
    globalLimit =       getAttrib(rootAttribs, 'limit',             DEFAULT_GLOBAL_LIMIT,       AttribType.INT)
    globalRepeat =      getAttrib(rootAttribs, 'repeat',            DEFAULT_GLOBAL_REPEAT,      AttribType.INT)
    globalPush =        getAttrib(rootAttribs, 'push',              DEFAULT_GLOBAL_PUSH,        AttribType.INT)
     
    if globalLimit>MAXLIMIT:
        globalLimit=MAXLIMIT
             
             
    sources = []
    #channelSources = _processChannels(xmlRoot.channels)
    #playlistSources = _processPlaylists(xmlRoot.playlists)
     
    for node in xmlRoot.children:
        print node
     
     
    types = {'channels':_processChannels, 'playlists':_processPlaylists}  #maybe move to bottom          
    for node in xmlRoot.children:           
                                      
        print node
         
        #get sources and their settings and set the global setting if not specified 
        #(which is possibly the default)
         
        nodeAttribs = node.attrib        
        limit =       getAttrib(nodeAttribs, 'limit',       globalLimit,       AttribType.INT)
        repeat =      getAttrib(nodeAttribs, 'repeat',      globalRepeat,      AttribType.INT)
        push =        getAttrib(nodeAttribs, 'push',        globalPush,        AttribType.INT)  
         
        if limit>MAXLIMIT:
            limit=MAXLIMIT                                                                                 
         
        #process according to the type of source                                                                                    
        sourceType = node.tag                                                                                                         
        nodeSources = types[sourceType](nodeAttribs, limit, repeat, push)
        sources.extend(nodeSources)
                 
          
         
     
    collection = Collection(title, thumb, sort, collectionLimit, unwatched, collectionFile, sources)                
     
    return collection
     
####################
## Private Methods##
####################     
def _processChannels(channels):
    pass
     
def _processPlaylists(playlists):
    pass
 
 
 
##old with ETree
# def _processChannels(attribs, limit, repeat, push):
#     sources = []
#     
#     usernames = attribs.get('user')
#     if usernames is not None:
#         usernames = usernames.split('|')
#         for username in usernames:
#             channel = Channel(limit, repeat, push, username=username)
#             sources.append(channel) 
#      
#              
#     ids = attribs.get('id')
#     if ids is not None:
#         ids = ids.split('|')
#         for channelId in ids:
#             channel = Channel(limit, repeat, push, channelId=channelId)
#             sources.append(channel)
# 
# 
#     return sources
#     
#     
# def _processPlaylists(attribs, limit, repeat, push):
#     sources = []
#     
#     ids = attribs.get('id')
#     ids = ids.split('|')
#     for playlistId in ids:
#         playlist = Playlist(playlistId, limit, repeat, push)
#         sources.append(playlist)
# 
#     return sources