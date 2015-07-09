import batchUpdater
from settings import globalCollection
from csource.KodiCollectionSource import KodiCollectionSource
from csource.YoutubeCollectionSource import YoutubeCollectionSource
from src.tools.enum import enum
from src import router
from src.tools.addonSettings import string as st
from src.videosource.VideoList import VideoList

from datetime import datetime, MINYEAR
from src.tools import pytz


loaded = {}


OnCollectionClick = enum(FEED=1, SOURCES=2, SOURCES_ONLY=3, PLAYALL=4)

GLOBAL_COLLECTION_FILE = 'globalCollection.xml'

D_TITLE = st(400)
D_THUMB = 'special://home/addons/plugin.video.collections/icon.png'
D_DEFAULT = False
D_ONCLICK = OnCollectionClick.FEED  #for global. for individual collection it's None


gc = None
class Collection(object):            
    def __init__(self, title, thumb, feedSettings, sourcesSettings, folderSettings, collectionFile, default=False, onClick=None):        
        self.title = title
        self.thumb = thumb
        self.default = default
        self._onClick = onClick      
                
        self.feedSettings = feedSettings
        self.sourcesSettings = sourcesSettings
        self.folderSettings = folderSettings
        
        self.file = collectionFile
        
        
        
        self.videos = None
        
         
        self.cSources = []
        self.cSourcesDic = {}
        self.numSources = 0
        
        self.cSourcesKodi = []
        self.cSourcesYt = []
        
        
        self.loadedSources = False
        
        #self.dumpFile = dumpFile
        #self.cachedXml = collectionFile.contents()

        


###################
## Public Methods##
###################
    def updateDatedSources(self, ytPages=1, forceUpdate=False):        
        batchUpdater.videoUpdate(self.cSourcesKodi, self.cSourcesYt, ytPages, forceUpdate)
        self.createCombinedList()



    def createCombinedList(self, customSort=None, reverse=None):
        combinedVideoList = VideoList( cSources=self.cSources, limit=self.feedSettings.limit() )
        
        vs = customSort if customSort else self.feedSettings.sort() 
        vs2 = self.feedSettings.sort2()
        reverse = reverse if reverse else self.feedSettings.reverseSort()
        
        combinedVideoList.sort(vs, vs2, reverse)
        combinedVideoList.applyLimits()
                
        self.videos = combinedVideoList        
        
        
        #     
#         if fs.unwatched():
#             for source in self.cSources:
#                 for video in source.allVideos():
#                     combinedVideoList.appendIfUnwatched(video)
#             
#         else:            
#             for source in self.cSources:
#                 for video in source.allVideos():
#                     combinedVideoList.append(video)

        
        #customSort if customSort else self.feedSettings.sort()
        
        
        
    
    
    def getCSource(self, sourceId):
        return self.cSourcesDic[sourceId]
        
#     def getCSourceIndex(self, index):
#         return self.cSources[index]
    
    
    def hasSource(self, sourceId):
        if sourceId in self.cSourcesDic:
            return True
        
        return False
        
    
        
        
        
    def addCollectionSource(self, vSource, onClick=None, limit=None, customTitle=None, customThumb=None, kodiEstimateDates=None):
        if vSource.isYoutube():
            cSource = YoutubeCollectionSource(self.numSources, self, vSource, onClick, limit, customTitle, customThumb)
            self.cSourcesYt.append(cSource)
                
        else:
            cSource = KodiCollectionSource(self.numSources, self, vSource, kodiEstimateDates, onClick, limit, customTitle, customThumb)
            self.cSourcesKodi.append(cSource)
        
        self.cSources.append(cSource)
        self.cSourcesDic[cSource.id] = cSource     
        self.numSources  += 1
        
        
    def setLoadedSources(self):
        self.loadedSources = True
        
    
    def removeCSource(self, sourceId):
        cSource = self.cSourcesDic.pop(sourceId)
        self.cSources.remove(cSource)
        
        if cSource.isKodiFolder():
            self.cSourcesKodi.remove(cSource)
        else:
            self.cSourcesYt.remove(cSource)
        
        
        
    
        
    def writeCollectionFile(self):
        if not self.loadedSources:
            raise ValueError ('Cannot write collection file when collection is not fully loaded!')
        
        from xml import exporter
        exporter.export(self)
            
    
                

    def onClick(self):
        return self._onClick if self._onClick else gc.onClick()








    def setTitle(self, title):
        self.title = title
        
    def setOnClick(self, onCollectionClick):
        self._onClick = onCollectionClick




    def playAllContextMenu(self):
        contextMenu =       (st(401),   'RunPlugin(%s)' % router.playCollectionUrl(self.file))
        return contextMenu

    def settingsContextMenu(self, globalC=False):
        if not globalC:
            contextMenu =   (st(402),   'RunPlugin(%s)' % router.editCollectionUrl(self.file))
        else:
            contextMenu =   (st(403),   'RunPlugin(%s)' % router.editCollectionUrl())
            
        return contextMenu

    def deleteContextMenu(self):
        contextMenu =       (st(404),   'RunPlugin(%s)' % router.deleteCollectionUrl(self.file))
        return contextMenu








def init():
    global gc
    
    if gc is None:
        gc = globalCollection.gc()
    
    





    

def empty(title, collectionFile):
    from settings import FeedSettings, SourcesSettings, FolderSettings
    global loaded
    
    fs  = FeedSettings.default() 
    ss  = SourcesSettings.default()
    fds = FolderSettings.default()
    
    collection = Collection(title, D_THUMB, fs, ss, fds, collectionFile)
    collection.setLoadedSources()
    
    loaded[collectionFile.fullpath] = collection    
    return collection
    

def emptyFromDirPath(title, dirPath):
    from src.file import File
    
    collectionFile = File.fromInvalidNameAndDir(title + '.xml', dirPath)    
    while collectionFile.exists():
        collectionFile =  File.fromNameAndDir(collectionFile.soleName + '_.xml', dirPath)
        
    return empty(title, collectionFile)
    
        
    
def fromFile(collectionFile, loadSources=True, isGlobal=False):    
    from xml import loader
    global loaded
        
    if collectionFile.fullpath in loaded:
        collection = loaded[collectionFile.fullpath]
        
        if (loadSources) and (not collection.loadedSources):
            loader.loadSources(collection)
                
        return collection
        
        
    collection = loader.load(collectionFile, loadSources, isGlobal)
    loaded[collectionFile.fullpath] = collection  
    
    return collection
        
   
      
                
#     def dump(self):
#         self.dumpFile.dumpObject(self)
        
        

#         self.cachedXml = self.file.contents()       #can use the filestring that is already in 
#                                                     #memory instead writing to drive and then 
#                                                     #loading back from drive.
#                                                     #but not sure, maybe safer this way
#         self.dump()


