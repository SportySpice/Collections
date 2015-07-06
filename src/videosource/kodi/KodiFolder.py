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


class KodiFolder(VideoSource):
    def __init__(self, path, title, thumb):
        self.path = path        
        #self.path = self.path.replace('\\', '/')        #HIGHLY UNSURE IF THIS WORKS FOR ALL CASES
        
        cacheFileName = str(uuid.uuid4()) + '.kfd'
        cacheFile = File.fromNameAndDir(cacheFileName, KODI_FOLDER_CACHE_DIR)
        self.cacheFile = cacheFile
        
        pathDic = DataDictionary.load(PATH_DIC_FILE, KODI_FOLDER_CACHE_DIR)
        pathDic.setIfNonExistent(path, cacheFile.fullpath)
        
        
        self._contentsUpdatedAt = None
        self._cacheMode = False
        self.updateInfo(title, thumb)
        
        
        global foldersLoaded
        foldersLoaded[path] = self
        
        
    def updateInfo(self, title, thumb):
        studioTitle = title         #maybe original's plugin name?
        tvShowTitle = title
        description = None 
               
           
        sourceType = SourceType.FOLDER
        sourceId = self.path
                
        super(KodiFolder, self).__init__(title, studioTitle, tvShowTitle, description, thumb, sourceType, sourceId)
       
        
        self.cache()



#####################
## Private Methods ##
#####################  
    def _list(self, mediaType=MediaType.VIDEO):
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
        videos = VideoList()
        videosDic = {}
        
        index = 0
        videoPosition = 1
        
        firstRun = True
        
        for response in nonEmptyResponses:        
            items = response['result']['files']
        
            for item in items:
                filetype = item['filetype']
                
                if filetype == 'directory':
                    if firstRun:
                        item = fromItem(item)
                        folders.append(item)
                        cacheableFolders.append((item.path, item.title, item.thumb, index))
                    
                
                elif filetype == 'file':
                    path = item['file']
                    if path in videosDic:       #this means the same video/media was already added in one of the other requests
                        continue
                    
                    item = KodiVideo(self, videoPosition, item)                    
                    videos.append(item)
                    videosDic[path] = item
                    videoPosition += 1
                    
                else:
                    raise ValueError('unknown filetype: %s' %filetype)
                
                allItems.append(item)
                index += 1
                
            firstRun = False
                
             
             
            
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
    def updateContents(self):
        return self._list()

        
        
    def updateContentsIfDated(self):
        if self.contentsNeedUpdate():
            self.updateContents()
    
        return self._listSuccess
    
    
    
    def updateContentsThread(self):
        return ContentsUpdater(self)
    

    
    
    
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
    
    
    
    
    
    
    def updatedContents(self, force=False):
        if force or self.contentsNeedUpdate():
            self.updateContents()
            
        return self.contents()
    
    
    def updatedVideos(self, force=False):
        return self.updatedContents()[1]
    
    
    
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
            index = folder[3]
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
            path, title, thumb, index = folder
            
            kodiFolder = fromPath(path, title, thumb)
            folders.append(kodiFolder)
            
            if self._allItems[index] is not None:
                raise ValueError('Index in allItems should be empty and reserved to the Kodi Folder loaded from cache')
                
            self._allItems[index] = kodiFolder

            
        self._folders = folders        
        self._cacheMode = False
        
        
        
    def browseUrl(self, root=False):
        return router.browseKodiFolderUrl(self.cacheFile, root)
    
    def browseOriginUrl(self):
        return self.path
    





class ContentsUpdater(threading.Thread):
    def __init__(self, kodiFolder):
        threading.Thread.__init__(self)
        self.kodiFolder = kodiFolder
        
    def run(self):
        self.kodiFolder.updateContents()
            
        
        




  

#############
## Helpers ##
#############  
def _processTitle(item):
    if item['title'] != '':
        return item['title']
    
    if item['label'] != '':
        return item['label']
    
    return ''







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
    
    
    pathDic = DataDictionary.load(PATH_DIC_FILE, KODI_FOLDER_CACHE_DIR)
    if pathDic.has(path):
        cacheFilePath = pathDic.get(path)
        cacheFile = File.fromFullpath(cacheFilePath)
        return fromCacheFile(cacheFile)

    
    return None



def fromItem(item):
    path = item['file']
    title = _processTitle(item)
    thumb = item['thumbnail']
    
    kodiFolder = _fromMemoryOrCache(path)
    if kodiFolder:
        kodiFolder.updateInfo(title, thumb)
        return kodiFolder

    
    
    return KodiFolder(path, title, thumb)        
    
    


def fromPath(path, title=None, thumb=None):
    kodiFolder = _fromMemoryOrCache(path)
    if kodiFolder:
        if title and not kodiFolder.title:      #not sure about this
            kodiFolder.updateInfo(title, thumb)
        return kodiFolder
    
    return KodiFolder(path, title, thumb)