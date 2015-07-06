from src.videosource.VideoList import vctToText, VideoCountType






class VideoVisual(object):
    def __init__(self, videoFTS, customVcts=None):
        self.videoFTS = videoFTS
        
        if customVcts:
            self.setCustomVcts(customVcts)
        
        else:
            self.countGetter,  self.maxChars,  self.textIfNone  = vctToText[VideoCountType.DATE]
            self.countGetter2, self.maxChars2, self.textIfNone2 = vctToText[VideoCountType.VIEWS]
    
    def setCustomVcts(self, customVcts):
        vct, vct2 = customVcts
            
        self.countGetter, self.maxChars, self.textIfNone = vctToText[vct]
        if vct2:
            self.countGetter2, self.maxChars2, self.textIfNone2 = vctToText[vct2]
        else:
            self.countGetter2, self.maxChars2, self.textIfNone2 = None, None, None
        
        
    
    def title(self, video):                
        countNumber  = self.countGetter(video)
        
        countNumber2 = self.countGetter2(video) if self.countGetter2 else None
        hasCount2    = True                     if self.countGetter2 else False
            
        return self.videoFTS.fullText(video.title, video.source.title, countNumber, self.maxChars, self.textIfNone, countNumber2, self.maxChars2, self.textIfNone2, hasCount2)
