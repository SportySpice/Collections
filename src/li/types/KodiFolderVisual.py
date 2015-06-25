class KodiFolderVisual(object):
    def __init__(self, textSettings):
        self.textSettings = textSettings
        
        
    def title(self, kodiFolder):
        return self.textSettings.apply(kodiFolder.title)