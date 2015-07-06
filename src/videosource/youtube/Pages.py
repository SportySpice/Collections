from datetime import datetime
from src.tools.enum import enum
from src.videosource.VideoSource import SourceType
from src.videosource.VideoList  import VideoSort
from src.videosource.youtube import batchUpdater
import service


ItemType = enum(VIDEO=0, VSOURCE=1)
TimeUnit = enum(SECONDS=0, MINUTES=1, HOURS=2, DAYS=3)

DEFAULT = 43967348623       #random hack


class Pages(object):
    def __init__(self, serviceRequest, responseProcess, itemType, contentTitle, defaultCacheTime, cacheTimeUnit, sourceObject, cacheAfterUpdates=True):
        self._serviceRequest = serviceRequest
        self._responseProcess = responseProcess
        self._itemType = itemType
        self._contentTitle = contentTitle       #for example "playlist videos" or "channel playlists"
        self._defaultCacheTime = defaultCacheTime
        self._defaultCacheTimeUnit = cacheTimeUnit
        
        self._sourceObject = sourceObject
        self._cacheAfterUpdates = cacheAfterUpdates

        self.clear()
        
    
        
    def clear(self):
        self._pages = []
        self._pagesReceived = 0
        self._cachedMode = False
        self._lastPageUpdated = None
        self._nextPageToken = None
        
        
        
        
        
####################
## Private Methods##
####################  
    def _updateRequest(self, pageNum):
        if pageNum==1:
            pageToken = None
            page = Page(pageToken, self._itemType)
            
        elif pageNum > self._pagesReceived:
            if pageNum != self._pagesReceived + 1:
                raise ValueError('Requested page: %s, but never even received the page before it. Last page received:%s' %(pageNum, self._pagesReceived))
            
            pageToken = self._nextPageToken
            page = Page(pageToken, self._itemType)
            
            
        else:
            page = self._pages[pageNum-1]
            pageToken = page.token 
            
        request = self._serviceRequest(pageToken)
        
        return request, page
        
        
        
        
    def _processResponse(self, response, pageNum, page):
        items = self._responseProcess(response)
        page.setItems(items)
        
        
        
        if pageNum > self._pagesReceived:
            if pageNum != self._pagesReceived + 1:
                raise ValueError('Received response for page: %s, but never even received the page before it. Last page received:%s' %(pageNum, self._pagesReceived))
            self._pages.append(page)
            self._pagesReceived = pageNum
            
            
        else:
            self._pages[pageNum-1] = page
            
            
        self._lastPageUpdated = pageNum
        self._nextPageToken = response.get('nextPageToken')
                
#         if pageNum == 1:            
#             self._allItems = items
#         else:
#             self._allItems.extend(items)


        if self._cacheAfterUpdates:
            self._sourceObject.cache()
        
        
        
    def _videoStatsRequest(self, videos):
        videoIds = ','.join(video.id for video in videos)         
        request = service.service().videos().list(part="snippet, contentDetails,statistics", id=videoIds, maxResults=50)
        
        return request
    
    
    def _processVideoStatsResponse(self, response, videos, pageNum):
        items = response.get("items", [])
        
        for i in range(len(videos)):
            video = videos[i]
            item = items[i]
            
            video.addInfo(item['contentDetails'], item['statistics'], item['snippet'])
            
        
        self._pages[pageNum-1].sortByDate()    #not sure if better to call this or keep original reported order
                                                
            
        if self._cacheAfterUpdates:
            self._sourceObject.cache()
        
        
        
###################
## Public Methods##
###################
    #can be any of the pages received so far, or 1 after (aka the next page) 
    #if 2 or more after is requested an error will raise  
    def updatePage(self, pageNum=1, fetchVideoStats=True):
        request, page = self._updateRequest(pageNum)
        response = request.execute()
        self._processResponse(response, pageNum, page)
        
        if self._itemType == ItemType.VIDEO and fetchVideoStats:
            self.fetchVideosStats(pageNum)



    def updatePageBatchRequest(self, pageNum=1):
        request, page = self._updateRequest(pageNum)
        
        def callback(request_id, response, exception):
            if exception:
                raise ValueError('Exception thrown in update %s http request from batch. Request ID: %s \nException: %s' %(self._contentTitle, request_id, exception))
            
            self._processResponse(response, pageNum, page)
                
        return (request, callback)
    
    def updatePageIfDated(self, pageNum=1, maxCacheTime=DEFAULT, cacheTimeUnit=DEFAULT, fetchVideoStats=True):
        if self.pageNeedsUpdate(pageNum, maxCacheTime, cacheTimeUnit):
            self.updatePage(pageNum, fetchVideoStats)

    
        
    def fetchNextPage(self, fetchVideoStats=True):
        pageNum = self._pagesReceived + 1
        self.updatePage(pageNum, fetchVideoStats)
    
    
    
    def fetchNextPageBatcchRequest(self):
        pageNum = self._pagesReceived + 1
        return self.updatePageBatchRequest(pageNum)
        
        
        
        
        
    def fetchVideosStats(self, pageNum=1):
        if self._itemType != ItemType.VIDEO:
            raise ValueError('Requested video statistics but item type is not videos')
        
        videos = self.pageItems(pageNum)
        request = self._videoStatsRequest(videos)
        
        response = request.execute()        
        self._processVideoStatsResponse(response, videos, pageNum)
        

        
        
        
    def fetchVideoStatsBatchRequest(self, pageNum):
        if self._itemType != ItemType.VIDEO:
            raise ValueError('Requested video statistics but item type is not videos')
        
        videos = self.pageItems(pageNum)
        request = self._videoStatsRequest(videos)
        
        def callback(request_id, response, exception):
            if exception:
                raise ValueError('Exception thrown in video stats http request from batch. Request ID: %s \nException: %s' %(request_id, exception))
            
            self._processVideoStatsResponse(response, videos, pageNum)
            
                
        return (request, callback)
        
        
        
        
    def hasNextPage(self):
        if self._nextPageToken:
            return True
        
        return False
    
    
    #returns true if already received page or if asked for next page and have a token for it
    #will raise an error if checked further than the next page
    def hasPage(self, pageNum):
        if pageNum > self._pagesReceived:
            if pageNum > self._pagesReceived + 1:
                raise ValueError('Cannot check more than one page forward. Pages recieved: %s, page asked about: %s' %self._pagesReceived, pageNum)
            if not self.hasNextPage():
                return False
            
        return True
            
    
    def lastPageUpdated(self):
        return self._lastPageUpdated
    
                
    def pagesRecieved(self):
        return self._pagesReceived
    
    def updatedPageAt(self, pageNum=1):
        page = self._pages[pageNum-1]
        return page.dateFetched    
    
        
    def pageNeedsUpdate(self, pageNum=1, maxCacheTime=DEFAULT, cacheTimeUnit=DEFAULT):
        if pageNum > self._pagesReceived:
            return True
        
        if maxCacheTime==DEFAULT:
            maxCacheTime = toSeconds[self._defaultCacheTimeUnit](self._defaultCacheTime())
        else:
            maxCacheTime = toSeconds[cacheTimeUnit](maxCacheTime)
                
        page = self._pages[pageNum-1]
        timePassed = datetime.now() - page.timeUpdated    
        if timePassed.seconds > maxCacheTime:
            return True
        
        return False
       
       
    
    def pageItems(self, pageNum=1, updateInfosIfNeeded=True):
        page = self._pages[pageNum-1]
        
        if updateInfosIfNeeded and self._itemType==ItemType.VSOURCE:
            batchUpdater.infoUpdate(page.items)
            
        
        return page.items
    
    
    def lastUpdateItems(self):
        return self.pageItems(self._lastPageUpdated)
    
    
    
    def updatedPageItems(self, pageNum=1, maxCacheTime=DEFAULT, cacheTimeUnit=DEFAULT, fetchVideoStats=True):
        self.updatePageIfDated(pageNum, maxCacheTime, cacheTimeUnit, fetchVideoStats)
        return self.pageItems(pageNum)
    
    
    
    
    

    
    
    
    
    
    
    
    def enterCachedModeAndCacheSourceObject(self):
        if self._itemType != ItemType.VSOURCE:
            raise ValueError('Item type is videos, no reason to go into cached mode')
        
        itemsList = []
        for page in self._pages:
            itemsList.append(page.items)
            page.items = None
        
        self._cachedMode = True
        self._sourceObject.cache(fromPages=True)
        
        for i in range(0, len(self._pages)):
            self._pages[i].items = itemsList[i]
            
        self._cachedMode = False
    
    
    
    
    def loadFromCachedMode(self):
        import Channel
        import Playlist
        
        
        if not self._cachedMode:
            raise ValueError('Cannot load from cached mode. Pages are not in cached mode')
        
        
        
        #sourcesToUpdate = []
        
        for page in self._pages:
            if page.items:
                raise ValueError('In cached mode, yet page has original videosource items')
            
            items = []
            for cachedItem in page.cacheableItems:
                if cachedItem[0] == SourceType.CHANNEL:
                    channelId = cachedItem[1] 
                    ytVideoSource, needsInfoUpdate = Channel.fromUserOrId(channelId=channelId)
                    
                else:
                    playlistId = cachedItem[1]
                    ytVideoSource, needsInfoUpdate = Playlist.fromPlaylistId(playlistId)
                    
                items.append(ytVideoSource)
                if needsInfoUpdate:     #ignored here
                    pass
                
                    
            page.items = items
            
        self._cachedMode = False
            
        
        

    
    
    
#     def updatedPageItems(self, pageNum=1, maxCacheTime=DEFAULT, cacheTimeUnit=DEFAULT, fetchVideoStats=True):
#         if pageNum > self._pagesReceived:
#             self.updatePage(pageNum, fetchVideoStats)
#             page = self._pages[pageNum-1]
#             
#             
#         else:
#             if maxCacheTime==DEFAULT:
#                 maxCacheTime =  toSeconds[self._defaultCacheTimeUnit](self._defaultCacheTime())
#             else:
#                 maxCacheTime = toSeconds[cacheTimeUnit](maxCacheTime)
#                 
#             page = self._pages[pageNum-1]
#             timePassed = datetime.now() - page.timeUpdated
#         
#             if timePassed.seconds > maxCacheTime:
#                 self.updatePage(pageNum, fetchVideoStats)
#                 
#                 
#                 
#         return page.videos
        #return self.pageVideos(pageNum) 
        
       
       

#     def allVideos(self):
#         return        
        
#     def rangeVideos(self, start, end):
#         return
        
        
        
        
        
class Page(object):
    def __init__(self, pageToken, itemType):
        self.token = pageToken
        self.itemType = itemType

        
    def setItems(self, items, timeUpdated=datetime.now()):
        self.items = items
        self.timeUpdated = timeUpdated
        #self.numItems = len(items)
        
        if self.itemType == ItemType.VSOURCE:
            cacheableItems = []
            for vSource in items:
                if vSource.isChannel():
                    item = (SourceType.CHANNEL, vSource.channelId)
                else:
                    item = (SourceType.PLAYLIST, vSource.playlistId)
                
                cacheableItems.append(item)
            
            self.cacheableItems = cacheableItems
            
    def sortByDate(self):
        if self.itemType != ItemType.VIDEO:
            raise ValueError('Page sorting is currently only supported for videos')
        
        
        self.items.sort(VideoSort.DATE)

        
        
def secondsToSeconds(seconds):
    return seconds
    
def minutesToSeconds(minutes):
    return minutes * 60

def hoursToSeconds(hours):
    return hours * 3600

def daysToSeconds(days):
    return days * 86400


        
toSeconds = {TimeUnit.SECONDS:secondsToSeconds, TimeUnit.MINUTES:minutesToSeconds, 
                      TimeUnit.HOURS:hoursToSeconds, TimeUnit.DAYS:daysToSeconds}    