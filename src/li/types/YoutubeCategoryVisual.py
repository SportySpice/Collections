class YoutubeCategoryVisual(object):
    def __init__(self, textSettings, customTitle=None, ctHasPageNum=False):
        self.textSettings = textSettings
        self.customTitle = customTitle
        self.ctHasPageNum = ctHasPageNum
        
        
        
    def title(self, category, pageNum):
        if self.customTitle:
            title = self.customTitle
            if self.ctHasPageNum:
                title = title %pageNum
                
        else:
            title = category.title
        
        title = self.textSettings.apply(title)
        return title