from src.tools.enum import enum

#VideoType = enum(PLUGIN=0, YOUTUBE=1)
OnVideoClick = enum (PLAY_ONLY=1, PLAY_QUEUE_REST=2)




class Video(object):
    def __init__(self, videoId, source, position, title, description, thumb, date, duration, rating):
        self.id = videoId
        #self.type = videoType
        
        self.source = source
        self.position = position
        self.title = title
        self.description = description
        self.thumb = thumb
        self.date = date
        self.duration = duration
        self.rating = rating


    
#     #abstract        
#     def resolvedUrl(self):
#         return

    #abstract
    def playUrl(self):
        return
    
    #abstract
    def watched(self):
        return
    
    #abstract (returns playCount, lastPlayed)
    def watchedInfo(self):
        return 
        
    def playCount(self):
        return self.watchedInfo()[0]
    
    def lastPlayed(self):
        return self.watchedInfo()[1]
    
    
    def isYoutube(self):
        return self.source.isYoutube()
    
    def isKodi(self):
        return self.source.isKodiFolder()