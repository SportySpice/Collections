class CollectionVisual(object):
    def __init__(self, textSettings, customTitle=None, customIcon=None, customThumb=None):
        self.textSettings = textSettings
        self.customTitle = customTitle
        self.customIcon = customIcon
        self.customThumb = customThumb        
        
             
                 
    def title(self, collection):
        if self.customTitle:
            title = self.customTitle
        else:
            title = collection.title
            
        title = self.textSettings.apply(title)
        return title
    
    
    def images(self, collection):
        if self.customIcon:
            icon  = self.customIcon
            thumb = self.customThumb
        
        else: 
            icon  = collection.thumb
            thumb = collection.thumb
            
        return icon, None