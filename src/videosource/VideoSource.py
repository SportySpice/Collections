from src.tools.enum import enum
from src.tools.addonSettings import string as st

SourceType = enum(  FOLDER=1,                       CHANNEL=2,                          PLAYLIST=3)
stToText   = {      SourceType.FOLDER:st(420),      SourceType.CHANNEL:st(421),         SourceType.PLAYLIST:st(422)}



 
class VideoSource(object):            
    def __init__(self, title, studioTitle, tvShowTitle, description, thumb, sourceType, sourceId):                        
        self.title = title
        self.studioTitle = studioTitle
        self.tvShowTitle = tvShowTitle        
        self.description = description
        
        self.thumb = thumb
        self.type = sourceType
        
        self.id = sourceId
        
        

        
###################
## Public Methods##
###################
    def isKodiFolder(self):
        if self.type == SourceType.FOLDER:
            return True
        
        return False
    
    
    def isChannel(self):
        if self.type == SourceType.CHANNEL:
            return True
        
        
    def isPlaylist(self):
        if self.type == SourceType.PLAYLIST:
            return True
    
    
    def isYoutube(self):
        if self.type == SourceType.CHANNEL or self.type==SourceType.PLAYLIST:
            return True
        
        return False
    
    def typeText(self):
        return stToText[self.type]
    
    def titles(self):
        return self.title, self.studioTitle, self.tvShowTitle
    
    
#    abstract
#    def browseUrl(self):
#        return
    
    
#     #abstract
#     def cache(self):
#         return







#     #abstract for youtube types
#     def fetchInfo(self):
#         return
#     
# 
#     #abstract for youtube types
#     def fetchInfoBatchRequest(self):        
#         return
#     
# 
#     #abstract for youtube types
#     def needsInfoUpdate(self):
#         return None