from src import router
from src.li.Li import Li



class VideoLi(Li):
    def __init__(self, video, url, isPlayable, videoVisual, collection=None):
        
        vSource = video.source
        if collection:
            cSource = collection.getCSource(vSource.id)
            sourceTitle, studioTitle, tvShowTitle = cSource.titles()
            thumb = cSource.thumb()
        else:
            sourceTitle, studioTitle, tvShowTitle = vSource.titles()
            thumb = video.thumb 
            
        title = videoVisual.title(video, sourceTitle)

        
        icon = None
        
        

        
        isFolder = False
        
        
        generalInfoLabels = self._generalInfoLabels(video)
        videoInfoLabels = self._videoInfoLabels(video, title, studioTitle, tvShowTitle)
        
        
        if collection: 
            if collection.default:
                contextMenus = (
                    collection.settingsContextMenu(globalC=True),
                )
            else:
                contextMenus = (
                    collection.settingsContextMenu(),
                    collection.settingsContextMenu(globalC=True)                        
                )
        else:
            contextMenus = None
        
        
        
        super(VideoLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels, contextMenus)


    
        self.pi = (url, self.li)    #needs to be unpacked when using with playlist.add()
        self.title = title
        self.thumb = thumb
        self.generalInfoLabels = generalInfoLabels
        self.videoInfoLabels = videoInfoLabels
    
        if video.duration:
            self.li.addStreamInfo('video', { 'duration': video.duration.seconds})
            
        
        
        
        
            
        
        
    
    @staticmethod
    def _generalInfoLabels(video):
        return {
            'date': video.date.strftime('%d.%m.%Y') if video.date else None,
            'Date': video.date.strftime('%d.%m.%Y') if video.date else None     #not sure if date or Date, check later
        }
    
    
        
    
    @staticmethod        
    def _videoInfoLabels(video, title, studioTitle, tvShowTitle):
        date = video.date
        
        
        return {
                'title':        title,
                #'originaltitle':video.title,
                'studio':       studioTitle,
                'tvshowtitle':  tvShowTitle,
                'plot':         video.description,
                
                
                
                
                'year':         date.year                   if date else None,
                'aired':        date.strftime('%Y-%m-%d')   if date else None,
                'premiered':    date.strftime('%Y-%m-%d')   if date else None,
                                                   
                'episode':      video.position,                                                                  
                'playcount':    video.playCount(),
                #'lastplayed': can use this, storing it already in watchedDic (string (%Y-%m-%d %h:%m:%s = 2009-04-05 23:16:04)
                
               
               'votes':     str(video.likeCount) if video.isYoutube() else None,
               'rating':    video.rating,
               
               
               
               #'duration': video.duration.seconds / 60
               
                #'status': 'Online!',            #(didn't work)                                   
                                                   
                
               
                #'album': ?            
                
                                                                                                                                                          
                #'tracknumber': maybe put position on original list                                    
                #'originaltitle': video.description    
                #'Tagline': video.description,
                #'Plotoutline': video.description,
                #'Season': ?                                    
    }
        
        
        
    






# def playKodiFolderLi(kodiVideo, videoVisual):        
#     url = router.playVideoKodiUrl(kodiVideoVideo.url)
#     isPlayable = True
#     
#     videoLi = VideoLi(KodiVideo, url, isPlayable, videoVisual) 
#     return videoLi    
#         
#         
# def playYoutubeLi(youtubeVideo, videoVisual):
#     url = router.playVideoYoutubeUrl(youtubeVideo.id)
#     isPlayable = True
#     
#     videoLi = VideoLi(youtubeVideo, url, isPlayable, videoVisual) 
#     return videoLi

def playVideoLi(video, videoVisual, collection=None):
    url = video.playUrl()
    isPlayable = True        
    videoLi = VideoLi(video, url, isPlayable, videoVisual, collection)
     
    return videoLi



def queuePlaylistLi(video, videoIndex, videoVisual, collection=None):
    url = router.playQueuePlaylistUrl(videoIndex)
    isPlayable = False
    
    videoLi = VideoLi(video, url, isPlayable, videoVisual, collection)    
    return videoLi


# def queueCollectionLi(video, collection, videoVisual):
#     url = router.playQueueCollectionUrl(video.id, collection.file)
#     isPlayable = False
#     videoLi = VideoLi(video, url, isPlayable, videoVisual, collection)
#      
#     return videoLi