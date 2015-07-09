import DataDictionary as dd
from src.file import File
from datetime import datetime



class WatchedDic(dd.DataDictionary):
    def __init__(self, dicFile):
        super(WatchedDic, self).__init__(dicFile)
    


    def watched(self, videoId):
        return self.has(videoId)



    def info(self, videoId):
        if not self.watched(videoId):
            return 0, None
                
        item = self.get(videoId)                
        playCount = item['plays']
        lastPlayed = item['lastPlayed']
        
        return playCount, lastPlayed
        
        
    def playCount(self, videoId):
        return self.info(videoId)[0]




    
    def videoPlayed(self, videoId):        
        if self.watched(videoId):
            item = self.get(videoId) 
            item['plays'] += 1
            
        else:
            item = {}
            item['plays'] = 1
            
        item['lastPlayed'] = datetime.now()
        
        self.set(videoId, item)



  

def load(fileName, fileDir):
    fullpath = fileDir + '/' + fileName
    
    watchedDic = dd._loadFromMemory(fullpath)
    if watchedDic:
        return watchedDic
    
    dicFile = File.fromFullpath(fullpath)
    return WatchedDic(dicFile)