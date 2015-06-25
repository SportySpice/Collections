class CustomFileVisual(object):
    def __init__(self, title, textSettings, icon, thumb):
        self._title = title
        self.textSettings = textSettings
        self.icon = icon
        self.thumb = thumb
        
        
        
    def title(self):
        return self.textSettings.apply(self._title)
    
    def images(self):
        return self.icon, self.thumb