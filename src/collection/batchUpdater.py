from src.videosource.kodi import batchUpdater as kodi
from src.videosource.youtube import batchUpdater as yt


def videoUpdate(cSourcesKodi, cSourcesYt, ytPages=1, forceUpdate=False):
    kodiFolders = []
    vSourcesYt = []
    
    for cSource in cSourcesKodi:
        kodiFolders.append(cSource.videoSource)
        
    for cSource in cSourcesYt:
        vSourcesYt.append(cSource.videoSource)
        
        
        
    kodiThread = kodi.contentsUpdateThread(kodiFolders, forceUpdate)
    ytThread = yt.videoUpdateThread(vSourcesYt, ytPages, forceUpdate)
    
    kodiThread.start()
    ytThread.start()
    
    kodiThread.join()
    ytThread.join()