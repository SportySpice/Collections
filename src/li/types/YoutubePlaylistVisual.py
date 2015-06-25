class YoutubePlaylistVisual(object):
    def __init__(self, textSettings, customTitle=None, ctHasPageNum=False, preTitle=None, 
                 preTitleTextSettings=None):
        self.textSettings = textSettings
        self.customTitle = customTitle
        self.ctHasPageNum = ctHasPageNum
        
        self.preTitle = preTitle
        self.preTitleTextSettings = preTitleTextSettings

        
        
    def title(self, playlist, pageNum):
        if self.customTitle:
            title = self.customTitle
            if self.ctHasPageNum:
                title = title %pageNum
        else:
            title = playlist.title
            
        if self.preTitle:
            preTitle = self.preTitleTextSettings.apply(self.preTitle)
            title = preTitle + title
        
        title = self.textSettings.apply(title)
        return title