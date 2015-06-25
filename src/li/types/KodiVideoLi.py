from src.li.Li import Li


class KodiVideoLi(Li):
    def __init__(self, kodiVideo, kodiVideoVisual):
        title = kodiVideoVisual.title(kodiVideo)   
        
        icon = kodiVideo.thumb
        thumb = None
        
        #url = router.browseKodiFolderUrl(kodiFolder.path)
        #url = ''
        url = kodiVideo.path
        
        isFolder = False
        isPlayable = True
            
        generalInfoLabels = None
        videoInfoLabels = None
 
    
        super(KodiVideoLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels)