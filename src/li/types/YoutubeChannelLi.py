from src.li.Li import Li
from src import router
import locale

locale.setlocale(locale.LC_ALL, '')

class YoutubeChannelLi(Li):
    def __init__(self, channel, youtubeChannelVisual, pageNum=1):
        #title = youtubeChannelVisual.title(channel, pageNum) +' ([COLOR red]{:,}[/COLOR])'.format(channel.subscriberCount)
        title = youtubeChannelVisual.title(channel, pageNum)  
        icon, thumb = youtubeChannelVisual.images(channel)          
        
        url = router.browseYoutubeChannelUrl(channel.cacheFile, pageNum)
        
        isFolder = True
        isPlayable = False
            
        generalInfoLabels = None
        videoInfoLabels = self._videoInfoLabels(channel)
 
    
        super(YoutubeChannelLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels)
        
        
        #self.li.setProperty('Episodes', '22')
        
        
        
    @staticmethod        
    def _videoInfoLabels(channel):
        #countsStr = '[B][COLOR red]{:,}[/B][/COLOR] subscribers. [B][COLOR red]{:,}[/B][/COLOR] videos.\n[B][COLOR red]{:,}[/B][/COLOR] Views. [B][COLOR red]{:,}[/B][/COLOR] comments.'.format(channel.subscriberCount, channel.videoCount, channel.viewCount, channel.commentCount)
        #description = countsStr + '\n\n' + channel.description
        
        return {
                #'title': ' ([COLOR red]{:,}[/COLOR]) '.format(channel.subscriberCount) + channel.title)
                'title': channel.title,
#                'studio': channel.studioTitle,
                #'tvshowtitle': channel.tvShowTitle,
                'plot': channel.description,
                
                #'episode': channel.videoCount
                
                #'year': date.year if date else None,
                #'aired': date.strftime('%Y-%m-%d') if date else None,
                #'premiered': date.strftime('%Y-%m-%d') if date else None,
                                                   
                                                                                  
                #'playcount': video.playCount()
                
                
                #'lastplayed': can use this, storing it already in watchedDic (string (%Y-%m-%d %h:%m:%s = 2009-04-05 23:16:04)
                
               
               
                #'status': 'Online!',            #(didn't work)                                   
                #'duration': duration in minutes                                   
                #'votes': number of thumbs up        
               
                #'album': ?            
                #'rating': maybe put some calculation between thumbs up and thumbs down  
                                                                                                                                                          
                #'tracknumber': maybe put position on original list                                    
                #'originaltitle': video.description    
                #'Tagline': video.description,
                #'Plotoutline': video.description,
                #'Season': ?                                    
    }