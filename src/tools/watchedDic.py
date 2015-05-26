from src.file import File
from datetime import datetime

WATCHED_DIC_FILE           = 'special://profile/addon_data/plugin.video.collections/watched.dic'


dicFile = File.fromFullpath(WATCHED_DIC_FILE)    

if dicFile.exists():
    watchedDic = dicFile.loadObject()    
else:
    watchedDic = {}
    




def videoPlayed(videoId):
    global dicFile
    global watchedDic
    
    if videoId in watchedDic:        
        watchedDic[videoId]['plays'] += 1
    else:
        watchedDic[videoId] = {}
        watchedDic[videoId]['plays'] = 1
        
    watchedDic[videoId]['lastplayed'] =  datetime.now()
    
        
    dicFile.dumpObject(watchedDic)



def watched(videoId):
    if videoId in watchedDic:
        return True
    
    return False    



def playCount(videoId):
    if videoId in watchedDic:
        return watchedDic[videoId]['plays']

    return 0
    
    
    
    

def info(videoId):
    if videoId in watchedDic:
        item = watchedDic[videoId]
        
        playCount = item['plays']
        lastPlayed = item['lastplayed']
        
        return playCount, lastPlayed
    
    
    return 0, None


 