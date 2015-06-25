class YoutubeChannelPlaylistsVisual(object):
    def __init__(self, title, tHasPageNum, textSettings, noThumb=True):
        self._title = title
        self.tHasPageNum = tHasPageNum
        self.textSettings = textSettings
        self.noThumb = noThumb
        
        
    def title(self, channel, pageNum):
        title = self._title
        if self.tHasPageNum:
            title = title %pageNum
            
        return self.textSettings.apply(title)
    
    
    def images(self, channel):
        if self.noThumb:
            return None, None
        
        icon = channel.thumb
        thumb = channel.thumb
            
        return icon, None