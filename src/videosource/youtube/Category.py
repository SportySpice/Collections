import service
import Channel
from src.file import File
from src.paths.root import CATEGORY_CACHE_DIR
from Pages import Pages, ItemType, TimeUnit
import settings as s


categoriesLoaded = {}


class Category(object):
    def __init__(self, categoryId, cacheFile, snippet):
        self.categoryId = categoryId
        self.title = snippet['title']
        
        self.channels = Pages(self._serviceRequest, self._responseProcess, ItemType.VSOURCE, 'category channels', s.categoryChannelsCacheTime, TimeUnit.DAYS, self)
        
        self.cacheFile = cacheFile        
        self.cache()
        
        
        global categoriesLoaded
        if categoryId in categoriesLoaded:
            raise ValueError('Category is in memory but with a different instance. This should never happen.')
        categoriesLoaded[categoryId] = self



    def cache(self, fromPages=False):
        if fromPages:
            self.cacheFile.dumpObject(self)
            return
        
        self.channels.enterCachedModeAndCacheSourceObject()
        


####################
## Private Methods##
####################         
    def _serviceRequest(self, pageToken):
        return service.service().channels().list(categoryId=self.categoryId, part='contentDetails,snippet,statistics', maxResults=50, pageToken=pageToken)
    
    def _responseProcess(self, response):
        channels = []
                
        for item in response['items']:
            channel = Channel.fromChannelsRequest(item)
            channels.append(channel)            
            
            
        return channels
    

def fromCacheFile(cacheFile):
    global categoriesLoaded
    
    category = cacheFile.loadObject()
    category.channels.loadFromCachedMode()
    
    if category.categoryId in categoriesLoaded:
        raise ValueError("Tried loading category from cache when it's already in memory")
    categoriesLoaded[category.categoryId] = category
    
    
    return category
    
    
    
def fromCategoryList(item):
    global categoriesLoaded
    
    categoryId = item['id']
    snippet = item['snippet']
    
    
    if categoryId in categoriesLoaded:
        return categoriesLoaded[categoryId]
    
    cacheFileName = categoryId + '.cat'
    cacheFile = File.fromNameAndDir(cacheFileName, CATEGORY_CACHE_DIR)
    
    if cacheFile.exists():
        category = fromCacheFile(cacheFile)
        return category
    
    return Category(categoryId, cacheFile, snippet)