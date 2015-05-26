import default_settings as d
from SourceSettings import SourceSettings
from Collection import Collection
from src.youtube.Channel import Channel
from src.youtube.Playlist import Playlist
from src.cxml.loader import rootAndChildren
from src.file import File


CACHE_DIR           = 'special://profile/addon_data/plugin.video.collections/cache/'
COLLECTION_DIC_FILE = 'special://profile/addon_data/plugin.video.collections/cache/__collections.dic'



def load(collectionFile):
    dicFile = File.fromFullpath(COLLECTION_DIC_FILE)
    if dicFile.exists():
        collectionDic = dicFile.loadObject()                    
        xmlFP = collectionFile.fullpath
                    
        if xmlFP in collectionDic:                      #check if this collection was ever cached
            dumpFileFP = collectionDic[xmlFP]
            dumpFile = File.fromFullpath(dumpFileFP)
                        
            collection = dumpFile.loadObject()
            
            if collection.cachedXml == collectionFile.contents():  #xml is same, we can use the data from before
                collection.fetchInfoIfTime()                       #unless a long time passed. if so, refetch it
                return collection                                  
            
            else:                                               #xml changed so we reload and redump the collection
                collection = _load(collectionFile, dumpFile)    #dic doesn't need to be touched
                return collection 
     
    else:
        collectionDic = {}
             
             
    
                                                        
    collection = _load(collectionFile)                                      #either there was no dic file at all, or collection
                                                                            #was never cached. we load the collection from 
    collectionDic[collectionFile.fullpath] = collection.dumpFile.fullpath   #scratch, find a new available dump file and dump it.
    dicFile.dumpObject(collectionDic)                                       #we also add it to the dic and dump/redump the dic
                                                             
    return collection



    
    
    
    
    
    
def _load(collectionFile, dumpFile=None):                
    root  = rootAndChildren(collectionFile)
    
    
    #get collection settings and set defaults if not specified
    title = root.text
    if title == '':
        title = d.TITLE
    
    settings = root.settings                                  
    collectionLimit =   settings.get(   'climit',       d.COLLECTION_LIMIT    )
    unwatched =         settings.get(   'unwatched',    d.UNWATCHED           )
    globalLimit =       settings.get(   'limit',        d.GLOBAL_LIMIT        )
    
    if globalLimit > d.MAX_LIMIT:
        globalLimit = d.MAX_LIMIT
            
            
    sources = []
    
    
    types = {'channels':_processChannel, 'playlists':_processPlaylist}  #maybe move to bottom    
    
    for node in root.children:
        sourceType = node.name
        
        for textRow in node.textRows:      
            sourceSettings = _processSourceSettings(textRow.settings, globalLimit)
            source = types[sourceType](textRow, sourceSettings)
        
            sources.append(source)
            
            
    
    if dumpFile is None:
        dumpFile = File.fromFullpath(CACHE_DIR + collectionFile.soleName + '.col')    
        while dumpFile.exists():
            dumpFile =  File.fromFullpath (dumpFile.path + '/' + dumpFile.soleName + '_' + '.col')
        
    
    collection = Collection(title, collectionLimit, unwatched, collectionFile, sources, dumpFile) 
    
       
    return collection    
    


#currently just limit, in the limit more things like repeat and push
def _processSourceSettings(settings, globalLimit):
    limit = settings.get('limit', globalLimit)        
        
    if limit > d.MAX_LIMIT:
        limit = d.MAX_LIMIT
        
    
    sourceSettings = SourceSettings(limit, None, None)    
    return sourceSettings
        



def _processChannel(textrow, sourceSettings):    
    user = textrow.text
    channelId = None
    
    settings = textrow.settings
    if settings.get('id', False):
        channelId = user
        user = None
                                        
        
    channel = Channel(sourceSettings, username=user, channelId=channelId)

    return channel
            




def _processPlaylist(textrow, sourceSettings):    
    playlistId = textrow.text                 
    playlist = Playlist(playlistId, sourceSettings)
        
    return playlist
    