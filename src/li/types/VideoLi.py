from src import router
from src.li.Li import Li



class VideoLi(Li):
    def __init__(self, video, url, isPlayable, videoVisual, collection=None):        
        title = videoVisual.title(video) 
        
        icon = video.thumb
        thumb = video.thumb 
        

        
        isFolder = False
        
        
        generalInfoLabels = self._generalInfoLabels(video)
        videoInfoLabels = self._videoInfoLabels(video, title)
        
        
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
    
        if video.duration:
            self.li.addStreamInfo('video', { 'duration': video.duration.seconds})
    
    
    @staticmethod
    def _generalInfoLabels(video):
        return {'Date': video.date.strftime('%d.%m.%Y') if video.date else None}
    
    
        
    
    @staticmethod        
    def _videoInfoLabels(video, title):
        source = video.source    
        date = video.date
        
        
        return {
                'title': title,
                'studio': source.studioTitle,
                'tvshowtitle': source.tvShowTitle,
                'plot': video.description,
                
                'year': date.year if date else None,
                'aired': date.strftime('%Y-%m-%d') if date else None,
                'premiered': date.strftime('%Y-%m-%d') if date else None,
                                                   
                'episode': video.position,                                                                  
                'playcount': video.playCount(),
                #'lastplayed': can use this, storing it already in watchedDic (string (%Y-%m-%d %h:%m:%s = 2009-04-05 23:16:04)
                
               
               'votes': video.likeCount if video.isYoutube() else None,
               'rating': video.rating,
               
               
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



def queueCollectionLi(video, collection, videoVisual):
    url = router.playQueueCollectionUrl(video.id, collection.file)
    isPlayable = False
    videoLi = VideoLi(video, url, isPlayable, videoVisual, collection)
     
    return videoLi