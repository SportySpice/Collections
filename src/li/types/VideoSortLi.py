from src import router
from src.li.Li import Li
from src.videosource.VideoSource import SourceType


class VideoSortLi(Li):
    def __init__(self, url, title, icon=None, thumb=None, contextMenus=None):
        
            
        
        isFolder = False
        isPlayable = False
            
        generalInfoLabels = None
        videoInfoLabels = None
 
    
        super(VideoSortLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels, contextMenus)
        
        
def collectionVideoSortLi(collection):
    url = router.sortVideolistUrl()
    title, icon, thumb = collection.feedSettings.TS.sortVisuals()
    
    
    if collection.default:
        contextMenus = (
            collection.settingsContextMenu(globalC=True),
        )
        
    else:
        contextMenus = (
            collection.settingsContextMenu(),
            collection.settingsContextMenu(globalC=True)
        )
        
    return VideoSortLi(url, title, icon, thumb, contextMenus)


def youtubeVideoSortLi(title):
    url = router.sortVideolistUrl(SourceType.CHANNEL)
    return VideoSortLi(url, title)

def kodiVideoSortLi(title):
    url = router.sortVideolistUrl(SourceType.FOLDER)
    return VideoSortLi(url, title)