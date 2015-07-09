from src.videosource.kodi import batchUpdater as kodi
from src.videosource.youtube import batchUpdater as yt


def videoUpdate(cSourcesKodi, cSourcesYt, ytPages=1, forceUpdate=False):
    kodiFolders = []
    estimateDateList = []
    
    vSourcesYt = []
    
    for cSource in cSourcesKodi:
        kodiFolders.append(cSource.videoSource)
        estimateDateList.append(cSource.estimateDates())
        
    for cSource in cSourcesYt:
        vSourcesYt.append(cSource.videoSource)
        
        
        
    kodiThread = kodi.contentsUpdateThread(kodiFolders, estimateDateList, forceUpdate)
    ytThread = yt.videoUpdateThread(vSourcesYt, ytPages, forceUpdate)
    
    kodiThread.start()
    ytThread.start()
    
    kodiThread.join()
    ytThread.join()