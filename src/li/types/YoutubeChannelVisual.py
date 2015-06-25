class YoutubeChannelVisual(object):
    def __init__(self, textSettings, customTitle=None, ctHasPageNum=False, noThumb=False, preTitle=None, 
                 preTitleTextSettings=None):
        self.textSettings = textSettings
        self.customTitle = customTitle
        self.ctHasPageNum = ctHasPageNum
        self.noThumb = noThumb
        
        self.preTitle = preTitle
        self.preTitleTextSettings = preTitleTextSettings
        
        
    def title(self, channel, pageNum):
        if self.customTitle:
            title = self.customTitle
            if self.ctHasPageNum:
                title = title %pageNum
        else:
            title = channel.title
            
        title = self.textSettings.apply(title)
        
        if self.preTitle:
            preTitle = self.preTitleTextSettings.apply(self.preTitle)
            title = preTitle + title
        
        return title
    
    
    def images(self, channel):
        if self.noThumb:
            return None, None
        
        icon = channel.thumb
        thumb = channel.thumb
            
        return icon, None