from src.li.Li import Li
from src import router

class YoutubePlaylistLi(Li):
    def __init__(self, playlist, youtubePlaylistVisual, pageNum=1):
        title = youtubePlaylistVisual.title(playlist, pageNum)   
        
        icon = playlist.thumb          
        thumb = None
        
        url = router.browseYoutubePlaylistUrl(playlist.cacheFile, pageNum)
        
        isFolder = True
        isPlayable = False
            
        generalInfoLabels = None
        videoInfoLabels = None
 
    
        super(YoutubePlaylistLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels)