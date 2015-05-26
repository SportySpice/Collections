class VideoVisual(object):
    def __init__(self, showSource, sourceTextSettings, titleTextSettings, imageSettings):
        self.showSource = showSource
        self.sourceTextSettings = sourceTextSettings
        self.titleTextSettings = titleTextSettings
        self.imageSettings = imageSettings
        
    
    def title(self, video):
        if self.showSource:
            sourceText = video.source.title + ": "
            sourceText = self.sourceTextSettings.apply(sourceText)
        else:
            sourceText = ''
        
        
        titleText = video.title
        titleText = self.titleTextSettings.apply(titleText)
        
        
        title = sourceText + titleText
        return title
    
    
    def images(self, video):
        icon = video.thumb.get(self.imageSettings.iconRes)
        thumb = video.thumb.get(self.imageSettings.iconRes)
        
        return icon, thumb