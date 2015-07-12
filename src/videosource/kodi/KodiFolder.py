import FolderRecord
import itemProcess
from src.videosource.VideoSource import VideoSource, SourceType
from src.videosource.VideoList import VideoList
from KodiVideo import KodiVideo
from src.paths.root import KODI_FOLDER_CACHE_DIR
from src.tools import DataDictionary
from src.file import File
import simplejson as json
from strings import jsonRpcDir
import xbmc
from src.tools.enum import enum
import uuid
from datetime import datetime
import settings as s
import threading
from src import router


PATH_DIC_FILE = '__pathes.dic'
MediaType = enum(VIDEO='video', MUSIC='music', PICTURES='pictures', FILES='files', PROGRAMS='programs')


foldersLoaded = {}
pathDic = DataDictionary.load(PATH_DIC_FILE, KODI_FOLDER_CACHE_DIR)


class KodiFolder(VideoSource):
    def __init__(self, path, title, thumb, description=None, date=None, dateType=None, duration=None, rating=None):
        studioTitle = title         #maybe original's plugin name?
        tvShowTitle = title
        
        sourceType = SourceType.FOLDER
        sourceId = path
        
        super(KodiFolder, self).__init__(title, studioTitle, tvShowTitle, description, thumb, sourceType, sourceId)
        
        
        self.path = path
        self.description = description
        self.date = date
        self.dateType = dateType
        self.duration = duration
        self.rating = rating
        
        
        
                
        #self.path = self.path.replace('\\', '/')        #HIGHLY UNSURE IF THIS WORKS FOR ALL CASES
        
        cacheFileName = str(uuid.uuid4()) + '.kfd'
        cacheFile = File.fromNameAndDir(cacheFileName, KODI_FOLDER_CACHE_DIR)
        self.cacheFile = cacheFile
                
        pathDic.setIfNonExistent(path, cacheFile.fullpath)
        
        
        self._contentsUpdatedAt = None
        self._cacheMode = False
        
        self.cache()
        
        global foldersLoaded
        foldersLoaded[path] = self
        
        
        
     

        
        
        
        
    def updateInfo(self, title, thumb, description=None, date=None, dateType=None, duration=None, rating=None):
        self.title = title
        self.studioTitle = title
        self.tvShowTitle = title
        
        self.thumb = thumb
                
        if description: self.description = description
        if duration:    self.duration = duration
        if rating:      self.rating = rating
                       
        if date:
            self.date = date
            self.dateType = dateType
        
        self.cache()
        
 



#####################
## Private Methods ##
#####################  
    def _list(self, estimateDates=False):
        requests = (
            jsonRpcDir(self.path, MediaType.VIDEO),
            jsonRpcDir(self.path, MediaType.MUSIC),
            jsonRpcDir(self.path, MediaType.PICTURES),
        )
        
        
        
        #get responses and check if there were no errors
        responses = []
        for request in requests:
            response = xbmc.executeJSONRPC(request)
            decodedResponse = json.loads(response)                        

            if 'error' in decodedResponse:
                self._allItems = None
                self._folders = None
                self._videos = None
                self._cacheableFolders = None 
                
                self._listSuccess = False
                self._empty = None
                self._contentsUpdatedAt = None
                self.cache()
                
                return False
            
            responses.append(decodedResponse)
            
                   
        #check which responses are empty (return if they all are)                 
        nonEmptyResponses = []
        for response in responses:
            if response['result']['limits']['total'] > 0:
                nonEmptyResponses.append(response)            
            
        if not nonEmptyResponses:
            self._allItems = None
            self._folders = None
            self._videos = None
            self._cacheableFolders = None 
            
            self._listSuccess = True
            self._empty = True
            self._contentsUpdatedAt =  datetime.now()
            self.cache()
            
            return True
        
        
        
        
        #process non empty responses
        allItems = []        
        folders = []        
        cacheableFolders = []        
        videos = VideoList(keepOriginalOrder=True)
        videosDic = {}
        
        index = 0
        videoPosition = 1
        
        firstRun = True
        
        if estimateDates:
            folderRecord = FolderRecord.fromPath(self.path)
            folderRecord.startEstimations()
        else:
            folderRecord = None
        
        for response in nonEmptyResponses:        
            items = response['result']['files']
        
            for item in items:
                filetype = item['filetype']
                
                if filetype == 'directory':
                    if firstRun:
                        f = fromItem(item)
                        folders.append(f)
                        cacheableFolders.append((index, f.path, f.title, f.thumb, f.description, f.date, f.dateType, f.duration, f.rating))
                        
                
                elif filetype == 'file':
                    path = item['file']
                    if path in videosDic:       #this means the same video/media was already added in one of the other requests
                        continue
                    
                    item = KodiVideo(self, videoPosition, item, folderRecord)                    
                    videos.append(item)
                    videosDic[path] = item
                    videoPosition += 1
                    
                else:
                    raise ValueError('unknown filetype: %s' %filetype)
                
                allItems.append(item)
                index += 1
                
            firstRun = False
                
        if estimateDates:
            folderRecord.endEstimations()     
             
            
        self._allItems = allItems
        self._folders = folders
        self._videos = videos
        self._cacheableFolders = cacheableFolders 
                
        self._listSuccess = True
        self._empty = False
        self._contentsUpdatedAt = datetime.now()
        
        
            
        self.cache()
    
            
        return True
        

####################
## Public Methods ##
####################    
    #override
    def updateContents(self, estimateDates=False):
        return self._list(estimateDates)

        
        
    def updateContentsIfDated(self, estimateDates=False):
        if self.contentsNeedUpdate():
            self.updateContents(estimateDates)
    
        return self._listSuccess
    
    
    
    def updateContentsThread(self, estimateDates=False):
        return ContentsUpdater(self, estimateDates)
    

    
    
    
    def updateFailed(self):
        return not self._listSuccess
    
    def isEmpty(self):
        return self._empty
    
    
    
    def contentsNeedUpdate(self):
        if self._contentsUpdatedAt is None:
            return True
        
        timePassed = datetime.now() - self._contentsUpdatedAt   
        if timePassed.seconds > s.kodiFolderCacheTime*60:
            return True
        
        return False
    
    
    
    def contents(self):
        return self._folders, self._videos, self._allItems
    
    def folders(self):
        return self._folders
    
    
    def videos(self):
        return self._videos
    
    
    
    
    
    
    def updatedContents(self, estimateDates=False, force=False):
        if force or self.contentsNeedUpdate():
            self.updateContents(estimateDates)
            
        return self.contents()
    
    
    def updatedVideos(self, estimateDates=False, force=False):
        return self.updatedContents(estimateDates)[1]
    
    
    
    def isKodiFolder(self):
        return True
    
    def isKodiVideo(self):
        return False
    
    
    
    
    def cache(self):
        if self._contentsUpdatedAt is None:
            self.cacheFile.dumpObject(self)
            return
        
        if self.updateFailed() or self.isEmpty():
            self.cacheFile.dumpObject(self)
            return
        
        folders = self._folders
        self._folders = None
            
            
        allItems = self._allItems        
        for folder in self._cacheableFolders:
            index = folder[0]
            self._allItems[index] = None
        
        
            
        
        
    
        self._cacheMode = True
        self.cacheFile.dumpObject(self)
        
        
        self._allItems = allItems
        self._folders = folders
        
        self._cacheMode = False
    
    
    
    
    def loadFromCacheMode(self):
        if self._contentsUpdatedAt is None:
            return
        
        
        if self.updateFailed() or self.isEmpty():
            return
        
        if not self._cacheMode:
            raise ValueError('Cannot load from cache mode. Kodi Folder is not in cache mode')
        
        folders = []
        
        for folder in self._cacheableFolders:
            index, path, title, thumb, description, date, dateType, duration, rating = folder 
            
            
            kodiFolder = fromPath(path, title, thumb, description, date, dateType, duration, rating)
            folders.append(kodiFolder)
            
            if self._allItems[index] is not None:
                raise ValueError('Index in allItems should be empty and reserved to the Kodi Folder loaded from cache')
                
            self._allItems[index] = kodiFolder

            
        self._folders = folders        
        self._cacheMode = False
        
        
        
    def browseUrl(self, root=False, estimateDates=False):
        return router.browseKodiFolderUrl(self.cacheFile, root=root, estimateDates=estimateDates)
    
    def browseOriginUrl(self):
        return self.path
    





class ContentsUpdater(threading.Thread):
    def __init__(self, kodiFolder, estimateDates=False):
        threading.Thread.__init__(self)
        self.kodiFolder = kodiFolder
        self.estimateDates = estimateDates
        
    def run(self):
        self.kodiFolder.updateContents(self.estimateDates)
            
        
        




  









###############
## Factories ##
###############     

def fromCacheFile(cacheFile):
    kodiFolder = cacheFile.loadObject()
    kodiFolder.loadFromCacheMode()
    
    global foldersLoaded
    if kodiFolder.path in foldersLoaded:
        raise ValueError("Tried loading kodi folder from cache when it's already in memory")
    foldersLoaded[kodiFolder.path] = kodiFolder
    
    return kodiFolder



def _fromMemoryOrCache(path):
    global foldersLoaded
    if path in foldersLoaded:
        return foldersLoaded[path]
    
    
    if pathDic.has(path):
        cacheFilePath = pathDic.get(path)
        cacheFile = File.fromFullpath(cacheFilePath)
        return fromCacheFile(cacheFile)

    
    return None



def fromItem(item):
    path, title, description, thumb, date, dateType, duration, rating = itemProcess.processAll(item)
    
    kodiFolder = _fromMemoryOrCache(path)
    if kodiFolder:
        kodiFolder.updateInfo(title, thumb, description, date, dateType, duration, rating)
        return kodiFolder
    
    return KodiFolder(path, title, thumb, description, date, dateType, duration, rating)        
    
    


def fromPath(path, title=None, thumb=None, description=None, date=None, dateType=None, duration=None, rating=None):
    kodiFolder = _fromMemoryOrCache(path)
    if kodiFolder:
        if title and not kodiFolder.title:      #not sure about this
            kodiFolder.updateInfo(title, thumb, description, date, dateType, duration, rating)
        return kodiFolder
    
    return KodiFolder(path, title, thumb, description, date, dateType, duration, rating)