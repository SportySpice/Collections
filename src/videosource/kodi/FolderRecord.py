from datetime import datetime, timedelta
from src.file import File
from src.paths.root import KODI_ESTIMATION_DIR
import uuid
from src.tools import DataDictionary
from src.tools import pytz

PATH_DIC_FILE = '__pathes.dic'


loaded = {}
pathDic = DataDictionary.load(PATH_DIC_FILE, KODI_ESTIMATION_DIR)       #from data file


class FolderRecord(object):
    def __init__(self, folderPath):
        self.folderPath= folderPath
                
        self.lastUpdate = None        
        self.fileName = None
        
        #self.videoRecords = []
        self.videoRecordsDic = {}
        
        
        
    def startEstimations(self):
        self.numEstimated = 0
            
    
    def getEstimation(self, videoId):
        if videoId in self.videoRecordsDic:
            videoRecord = self.videoRecordsDic[videoId]
            return videoRecord.estimated             
            
        
        firstSeen = datetime.now(pytz.utc)
        firstSeen += timedelta(milliseconds=self.numEstimated)          #we mark each date as one ms after another 
        videoRecord = VideoRecord(self.lastUpdate, firstSeen)           #so sort by date keeps their order
    
        #self.videoRecords.append(videoRecord)
        self.videoRecordsDic[videoId] = videoRecord
                    
        self.numEstimated += 1
        return videoRecord.estimated
    
    

            
        
        
        
        
    def endEstimations(self):
        if self.lastUpdate is None:
            if (self.numEstimated == 0):        #this folder was never saved before and didn't add any records either
                return                          #so no need to save it. if it was saved before and added no records
                                                #we still need to save it just to mark the new time of lastUpdate
                                                
            fileName = str(uuid.uuid4()) + '.fde'
            self.fileName = fileName        
            recordFile = File.fromNameAndDir(fileName, KODI_ESTIMATION_DIR)            
            pathDic.setIfNonExistent(self.folderPath, recordFile.fullpath)
                                   
                           
        else:
            recordFile = File.fromNameAndDir(self.fileName, KODI_ESTIMATION_DIR)
            
            
        
        
        
        self.lastUpdate = datetime.now(pytz.utc)  
        del self.numEstimated
        
        
        recordFile.dumpObject(self)
                
            
            
        

class VideoRecord(object):
    def __init__(self, lastFolderUpdate, firstSeen):
        self.firstSeen = firstSeen
        self.lastFolderUpdate = lastFolderUpdate
        
        if lastFolderUpdate:
            difference = firstSeen - lastFolderUpdate
            self.estimated = lastFolderUpdate + (difference/2)
        else:
            self.estimated = None
        
        
        
        
        

    
    

def fromPath(folderPath):
    global loaded
    
    if folderPath in loaded:                                                #from memory
        return loaded[folderPath]
        
    if pathDic.has(folderPath):
        recordFilePath = pathDic.get(folderPath)
        recordFile = File.fromFullpath(recordFilePath)        
        folderRecord = recordFile.loadObject()        
        
        if folderRecord.folderPath in loaded:
            raise ValueError("Tried loading folder record from file when it's already in memory")
        
    
    else:                                                                   #create new
        folderRecord = FolderRecord(folderPath)
    

    loaded[folderRecord.folderPath] = folderRecord
    return folderRecord