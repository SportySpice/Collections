class VideoVisual(object):
    def __init__(self, videoFTS):
        self.videoFTS = videoFTS
        
        #self.imageSettings = imageSettings        
        
        
    
    def title(self, video):
        if video.isYoutube():
            return self.videoFTS.fullText(video.title, video.source.title, video.viewCount)
        else:
            return self.videoFTS.fullText(video.title, video.source.title)
        
        
        
    
#     def description(self, video):
#         if video.isKodiFolder():
#             return video.description
        
        
    
    
    
#     def images(self, video):
#         icon = video.thumb.get(self.imageSettings.iconRes)
#         thumb = video.thumb.get(self.imageSettings.iconRes)
#         
#         return icon, thumb