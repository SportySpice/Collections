class SourceVisual(object):
    def __init__(self, textSettings, imageSettings):
        self.textSettings = textSettings
        self.imageSettings = imageSettings
        
    def title(self, source):
        return self.textSettings.apply(source.title)
        
        
    def images(self, source):
        icon = source.thumb.get(self.imageSettings.iconRes)
        #thumb = source.thumb.get(self.imageSettings.iconRes)
        
        return icon, None