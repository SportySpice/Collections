import itemProcess
from src.videosource.Video import Video
from src import router
from src.tools import WatchedDic
from src.paths.root import KODI_DATA_DIR



        


WATCHED_DIC_FILE           = 'watched.dic'
watchedDic = WatchedDic.load(WATCHED_DIC_FILE, KODI_DATA_DIR)


class KodiVideo(Video):
    def __init__(self, kodiFolder, position, item, folderRecord=None):
        path, title, description, thumb, date, dateType, duration, rating = itemProcess.processAll(item, folderRecord)        
        videoId = path        
        super(KodiVideo, self).__init__(videoId, kodiFolder, position, title, description, thumb, date, duration, rating, watchedDic)
        
        self.path = path
        self.dateType = dateType


    #override
    def playUrl(self):
        return router.playVideoKodiUrl(self.path)

        


    
    def isKodiVideo(self):
        return True
        
    def isKodiFolder(self):
        return False
    
    






