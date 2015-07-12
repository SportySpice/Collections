from src.videosource.kodi import KodiFolder
from src.tools import videoResolve
from src.videosource.kodi.FolderVideo import ParseMethod, fifWatchedDic





def play(kodiFolderFile, parseMethod):
    kodiFolder = KodiFolder.fromCacheFile(kodiFolderFile)
    
    if parseMethod == ParseMethod.FIRST_IN_FOLDER:
        videos = kodiFolder.updatedVideos()
    
        if kodiFolder.updateFailed():
            return                      #not sure what to do here yet
        
        #if (kodiFolder.isEmpty()) or (not videos):
        if not videos:
            return                      #same
    
        video = videos[0]
        
        videoResolve.resolve(video.path)
        fifWatchedDic.videoPlayed(video.path)
        
        
#     elif parseMethod == ParseMethod.FOLDERS_AS_VIDEOS:      #this doesn't work for now, maybe make it
#         videoResolve.resolve(kodiFolder.path)               #work in the future somehow
#         favWatchedDic.videoPlayed(kodiFolder.path)