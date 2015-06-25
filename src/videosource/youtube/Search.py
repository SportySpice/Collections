import service
import Playlist
import Channel
from settings import regionCode
from src.tools.enum import enum
from Pages import Pages, ItemType, TimeUnit
import settings as s
from src.file import File
from src.paths.root import SEARCH_CACHE_DIR
import uuid



SearchType = enum(CHANNEL='channel', PLAYLIST='playlist', BOTH='channel,playlist')


class Search(object):
    def __init__(self, query, searchType):
        self.query = query
        self.searchType = searchType
        
        self.results = Pages(self._serviceRequest, self._responseProcess, ItemType.VSOURCE, '%s search results' %searchType, s.searchesCacheTime, TimeUnit.MINUTES, self)
        
        cacheFileName = str(uuid.uuid4()) + '.srch'
        self.cacheFile = File.fromNameAndDir(cacheFileName, SEARCH_CACHE_DIR)
        
        
        
    def cache(self, fromPages=False):
        if fromPages:
            self.cacheFile.dumpObject(self)
            return
        
        self.results.enterCachedModeAndCacheSourceObject()
        
        
         
    
         
         
         
         
####################
## Private Methods##
####################          
    def _serviceRequest(self, pageToken):
        return service.service().search().list(q=self.query, part='snippet', type=self.searchType, regionCode=regionCode, maxResults=50, pageToken=pageToken)
        
    
    def _responseProcess(self, response):
        results = []        
        
        items = response['items']
        
        for item in items:
            kind = item['id']['kind']
            
            if kind == 'youtube#channel':
                channel = Channel.fromSearchRequest(item)
                results.append(channel)
                
            elif kind == 'youtube#playlist':
                playlist = Playlist.fromSearchRequest(item)
                results.append(playlist)
                
            else:
                raise ValueError('Unknown kind in youtube search: %s' %kind)
                
        
                        
        return results
    
    
    
def fromCacheFile(cacheFile):
    search = cacheFile.loadObject()
    search.results.loadFromCachedMode()
    
    return search