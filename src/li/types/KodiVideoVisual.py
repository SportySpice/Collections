class KodiVideoVisual(object):
    def __init__(self, textSettings):
        self.textSettings = textSettings
        
        
    def title(self, kodiFile):
        return self.textSettings.apply(kodiFile.title)