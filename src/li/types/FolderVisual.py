class FolderVisual(object):
    def __init__(self, textSettings, customTitle=None, customIcon=None, customThumb=None):        
        self.textSettings = textSettings
        self.customTitle = customTitle
        self.customIcon = customIcon
        self.customThumb = customThumb
        
    
    
    def title(self, folder):
        if self.customTitle is not None:
            title = self.customTitle
        else:
            title = folder.name
            
        title = self.textSettings.apply(title)
        return title
    
    
    
    def images(self, folder):
        if self.customIcon is not None or self.customThumb is not None:
            return self.customIcon, self.customThumb
        
        
        
        if folder.hasSubfolder('_images'):
            imageFolder = folder.getSubfolder('_images')
            
            if imageFolder.hasFile('_folder.png'):
                return imageFolder.getFile('_folder.png').fullpath, None    #thumb not used for now
            
            elif imageFolder.hasFile('_folder.jpg'):
                return imageFolder.getFile('_folder.jpg').fullpath, None    #thumb not used for now
            
            
        return None, None