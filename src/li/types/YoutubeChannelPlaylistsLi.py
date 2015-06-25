from src.li.Li import Li
from src import router

class YoutubeChannelPlaylistsLi(Li):
    def __init__(self, channel, youtubeChannelPlaylistsVisual, pageNum=1):
        title = youtubeChannelPlaylistsVisual.title(channel, pageNum)   
        icon, thumb = youtubeChannelPlaylistsVisual.images(channel)          
        
        url = router.browseYoutubeChannelPlaylistsUrl(channel.cacheFile, pageNum)
        
        isFolder = True
        isPlayable = False
            
        generalInfoLabels = None
        videoInfoLabels = None
 
    
        super(YoutubeChannelPlaylistsLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels)