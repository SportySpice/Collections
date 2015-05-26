import datetime
from Thumb import Thumb

class Video(object):
    
    def __init__(self, playlistItemSnippet, position=None, source=None):
        snippet = playlistItemSnippet
        
        self.title = snippet['title']
        self.description = snippet['description']
        self.id = snippet['resourceId']['videoId']
        self.thumb = Thumb(snippet['thumbnails'])          
        
        self.channelTitle = snippet['channelTitle']
                
        self.position = position
        self.source=source
        
        #published date
        publishedAt = snippet['publishedAt']
        date, time = publishedAt.split('T', 1)
        #time, unknown = time.split('.', 1) 
        time = time.split('.', 1)[0]
        
        year,month,day = date.split('-', 2)
        hour,minute,second = time.split(':', 2)
        
        self.publishedDate = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        
        
        
    def fullUrl(self):
        return "https://www.youtube.com/watch?v=" + self.id