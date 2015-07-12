from src.videosource.Video import Video
from src import router
from src.tools import WatchedDic
from src.paths.root import KODI_DATA_DIR
from src.tools.enum import enum

ParseMethod = enum(NORMAL=1, FIRST_IN_FOLDER=2, FOLDERS_AS_VIDEOS=3)



FIRST_IN_FOLDER_WATCHED_DIC_FILE        = 'watched_first_in_folder.dic'
#FOLDERS_AS_VIDEOS_WATCHED_DIC_FILE      = 'watched_folders_as_videos.dic'

fifWatchedDic = WatchedDic.load(FIRST_IN_FOLDER_WATCHED_DIC_FILE, KODI_DATA_DIR)
#favWatchedDic = WatchedDic.load(FOLDERS_AS_VIDEOS_WATCHED_DIC_FILE, KODI_DATA_DIR)





class FolderVideo(Video):
    def __init__(self, sourceFolder, position, kodiFolder, parseMethod):        
        videoId     = kodiFolder.path
        
        title       = kodiFolder.title
        description = kodiFolder.description
        thumb       = kodiFolder.thumb
        
        date        = kodiFolder.date        
        duration    = kodiFolder.duration
        rating      = kodiFolder.rating        
        
        if parseMethod      == ParseMethod.FIRST_IN_FOLDER:     watchedDic = fifWatchedDic
        #elif parseMethod    == ParseMethod.FOLDERS_AS_VIDEOS:   watchedDic = favWatchedDic
        else: raise ValueError('FolderVideo have normal parse method')
        
        super(FolderVideo, self).__init__(videoId, sourceFolder, position, title, description, thumb, date, duration, rating, watchedDic)
        

        self.kodiFolder = kodiFolder
        self.parseMethod = parseMethod

    #override
    def playUrl(self):
        return router.playVideoKodiFolderUrl(self.kodiFolder.cacheFile, self.parseMethod)

        


    
    def isKodiVideo(self):
        return True
        
    def isKodiFolder(self):
        return False
    
    






