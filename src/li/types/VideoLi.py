from src import router
from src.li.Li import Li
from src.tools import watchedDic


class VideoLi(Li):
    def __init__(self, video, videoVisual, special=False, collectionFile=None,
                  sourceSpecial=False, sourceId=None):
        
        title = videoVisual.title(video)
        icon, thumb = videoVisual.images(video) 
        
        if special:
            url = router.playVideoSpecialUrl(video.id, collectionFile)
            isPlayalbe = False
        elif sourceSpecial:
            url = router.playVideoSourceUrl(video.id, sourceId, collectionFile)
            isPlayalbe = False
        else:
            url = router.playVideoUrl(video.id)
            isPlayalbe = True
        
        isFolder = False
        
        
        generalInfoLabels = self._generalInfoLabels(video)
        videoInfoLabels = self._videoInfoLabels(video, title)
        
        
        super(VideoLi, self).__init__(title, icon, thumb, url, isFolder, isPlayalbe,
                                       videoInfoLabels, generalInfoLabels)


    
        self.pi = (url, self.li)    #needs to be unpacked when using with playlist.add()
    
    
    
    
    @staticmethod
    def _generalInfoLabels(video):    
        return {'Date': video.publishedDate.strftime('%d.%m.%Y')}
    
    
        
    
    @staticmethod        
    def _videoInfoLabels(video, title):        
        date = video.publishedDate        
        playCount, lastPlayed = watchedDic.info(video.id)
        
        return {
                'title': title,                                                            
                'plot': video.description,
                'year': date.year,
                'studio': video.channelTitle,
                'aired': date.strftime('%Y-%m-%d'),                                   
                'tvshowtitle': video.source.title2,
                'episode': video.position,    
                                                                              
                'playcount': playCount
                #'lastplayed': maybe store last time played (string (%Y-%m-%d %h:%m:%s = 2009-04-05 23:16:04)
               
               
                #'status': 'Online!',            #(didn't work)                                   
                #'duration': duration in minutes                                   
                #'votes': number of thumbs up        
               
                #'album': ?            
                #'rating': maybe put some calculation between thumbs up and thumbs down  
                #'premiered': date.strftime('%Y-%m-%d')                                                                                                                                          
                #'tracknumber': maybe put position on original list                                    
                #'originaltitle': video.description    
                #'Tagline': video.description,
                #'Plotoutline': video.description,
                #'Season': ?                                    
    }