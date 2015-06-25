import service
import Channel
from Pages import Pages, ItemType, TimeUnit
from src.file import File
from src.paths.root import YOUTUBE_CACHE_DIR
from src.tools.enum import enum
import settings as s


SubscriptionSorting = enum(ALPHABETICAL='alphabetical', RELEVANCE='relevance', UNREAD='unread')






CACHE_FILE = 'subscriptions.sub' 


loaded = None


class Subscriptions:
    def __init__(self, cacheFile):                
        self.channels = Pages(self._serviceRequest, self._responseProcess, ItemType.VSOURCE, 'subscription channels', s.subscriptionChannelsCacheTime, TimeUnit.DAYS, self)
        
        
        self.cacheFile = cacheFile
        self.order = s.subscriptionSorting()
        
        global loaded
        if loaded:
            raise ValueError('Subscriptions is in memory but with a different instance. This should never happen.')
        loaded = self
        
    
    
    def cache(self, fromPages=False):
        if fromPages:
            self.cacheFile.dumpObject(self)
            return
        
        self.channels.enterCachedModeAndCacheSourceObject()


        
    def checkSettingsChange(self):
        setting = s.subscriptionSorting()
        
        if self.order != setting:
            self.order = setting
            self.channels.clear()
            self.cache()
    
    
    
    
####################
## Private Methods##
#################### 
    def _serviceRequest(self, pageToken):
        return service.service().subscriptions().list(mine=True, part='snippet, contentDetails', order=self.order, pageToken=pageToken, maxResults=50)
      
    @staticmethod
    def _responseProcess(response):  
        channels = []
        items = response['items']    
            
        for item in items:
            channel = Channel.fromSubscriptionsRequest(item)
            channels.append(channel)
            
        return channels
    
    



def load():
    global loaded
    if loaded:
        loaded.checkSettingsChange()
        return loaded
    
    cacheFile = File.fromNameAndDir(CACHE_FILE, YOUTUBE_CACHE_DIR)
    if cacheFile.exists():
        subscriptions = cacheFile.loadObject()
        subscriptions.channels.loadFromCachedMode()
        subscriptions.checkSettingsChange()
        loaded = subscriptions
        
        return subscriptions
    
    return Subscriptions(cacheFile)