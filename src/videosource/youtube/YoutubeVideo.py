import datetime
from Thumb import Thumb
from src.videosource.Video import Video
from settings import videoThumbres
from src import router
from src.tools import WatchedDic
from src.paths.root import YOUTUBE_DATA_DIR
from src.tools.isodate import isoduration, isodatetime


WATCHED_DIC_FILE           = 'watched.dic'
watchedDic = WatchedDic.load(WATCHED_DIC_FILE, YOUTUBE_DATA_DIR)


class YoutubeVideo(Video):    
    def __init__(self, source, position, snippet):        
        youtubeThumb = Thumb(snippet['thumbnails'])        
        videoId= snippet['resourceId']['videoId']
                
        title = snippet['title']
        description = snippet['description']
        thumb = youtubeThumb.get(videoThumbres)
        #date = _processDate(snippet)
        date = isodatetime.parse_datetime(snippet['publishedAt'])
        
        self.viewCount = None
        self.likeCount = None
        self.dislikeCount = None
        self.commentCount = None    
        

        
        #self.youtubeThumb = youtubeThumb        
        #self.channelTitle = snippet['channelTitle']
        
        duration = None #need another api request for this and call addInfo()
        rating = None   #same                  
                
        super(YoutubeVideo, self).__init__(videoId, source, position, title, description, thumb, date, duration, rating, watchedDic)
        
        
    
    def addInfo(self, contentDetails, statistics, snippet):        
        self.duration = isoduration.parse_duration(contentDetails['duration'])
                        
        self.viewCount = int(statistics['viewCount'])
        self.commentCount = int(statistics['commentCount'])
        
        likeCount = int(statistics['likeCount'])
        dislikeCount = int(statistics['dislikeCount'])
        self.likeCount = likeCount
        self.dislikeCount = dislikeCount        
        
        if likeCount>0:
            self.rating = (likeCount / float((likeCount + dislikeCount))) * 10
        else:
            self.rating = 0 if dislikeCount > 0     else None
            #self.rating = 0
                
            
            
        self.date = isodatetime.parse_datetime(snippet['publishedAt'])  #date from this request is more accurate as the other request
                                                                        #gives the date the video was added to playlist instead of
                                                                        #when it went public as seen on youtube site
        
    def fullUrl(self):
        return "https://www.youtube.com/watch?v=" + self.id
    
    
    
    #override
    def playUrl(self):
        return router.playVideoYoutubeUrl(self.id)
    
#     #override
#     def resolvedUrl(self):
#         import urlResolver
#         streamurl = urlResolver.resolve(self.id)
#         return streamurl
    
    
    
    
    
    
    
def _processDate(snippet):
    publishedAt = snippet['publishedAt']
    date, time = publishedAt.split('T', 1)
    #time, unknown = time.split('.', 1) 
    time = time.split('.', 1)[0]
        
    year,month,day = date.split('-', 2)
    hour,minute,second = time.split(':', 2)
        
    date = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    
    return date