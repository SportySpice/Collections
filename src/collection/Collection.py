from apiclient.http import BatchHttpRequest
from datetime import datetime
from src.tools import watchedDic


FETCH_INFO_DELTA        =   7                   #in days
VIDEOS_UPDATE_DELTA     =   300                 #in seconds. 300 seconds = 5 minutes


#Sort = enum(NEWEST='newest', SHUFFLE='shuffle')




class Collection(object):            
    def __init__(self, title, collectionLimit, unwatched, collectionFile, sources, dumpFile):
        self.videoList = None        
        self.title = title
        self.collectionLimit = collectionLimit
        self.unwatched = unwatched
        self.file = collectionFile
        self.sources = sources
        
        self.dumpFile = dumpFile
        self.cachedXml = collectionFile.contents()
        
        self.fetchInitialInfo()
        self.updateVideoList()



###################
## Public Methods##
###################                 
    def fetchInitialInfo(self):        
        batch = BatchHttpRequest()
        for source in self.sources:
            request, callback = source.getInitialRequest()            
            batch.add(request, callback=callback)
            #batch.add(*source.getInitialRequest())
 
        batch.execute()
        #batch.execute(http=request.http)
        
        sourceDic = {}
        for source in self.sources:
            sourceDic[source.id] = source
        self.sourceDic = sourceDic
        
         
        self.fetchedInfoAt = datetime.now()
        self.dump()
        
        
    def fetchInfoIfTime(self):
        lastFetchDelta = datetime.now() - self.fetchedInfoAt
        
        if lastFetchDelta.days > FETCH_INFO_DELTA:
            self.fetchInitialInfo()
        
        
        
        
 

    def updateVideoList(self):
        batch = BatchHttpRequest()
        for source in self.sources:
            request, callback = source.getUpdateRequest()
            batch.add(request, callback=callback)
            #batch.add(*source.getUpdateRequest())
 
        batch.execute()
        #batch.execute(http=request.http)
         
         
                     
        combinedVideoList = []
        
        if self.unwatched:
            for source in self.sources:
                for video in source.videos():
                    if not watchedDic.watched(video.id):
                        combinedVideoList.append(video)
            
        else:
            for source in self.sources:
                for video in source.videos():
                    combinedVideoList.append(video)


        combinedVideoList.sort(key = lambda video: video.publishedDate, reverse=True)
                
        
        
        listLength = len(combinedVideoList)        
        if listLength > self.collectionLimit:                        
            extraItems = listLength - self.collectionLimit
            del combinedVideoList[-extraItems:]
            
        
        
        self.videoList = combinedVideoList        
        self.updatedVideosAt = datetime.now()
        
        self.dump()
        
        
    def updateVideosIfTime(self):
        lastUpdateDelta = datetime.now() - self.updatedVideosAt
        
        if lastUpdateDelta.seconds > VIDEOS_UPDATE_DELTA:
            self.updateVideoList()
        
    
    
    def getSource(self, sourceId):
        return self.sourceDic[sourceId]
        
        
    
    
    def dump(self):
        self.dumpFile.dumpObject(self)