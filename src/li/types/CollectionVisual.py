class CollectionVisual(object):
    def __init__(self, textSettings, defaultIcon, defaultThumb, forceDefaultImages, customTitle=None):
        self.textSettings = textSettings
        self.defaultIcon = defaultIcon
        self.defaultThumb = defaultThumb
        self.forceDefaultImages = forceDefaultImages
        self.customTitle = customTitle
             
                 
    def title(self, collectionRoot):
        if self.customTitle is not None:
            title = self.customTitle
        else:
            title = collectionRoot.text
            
        title = self.textSettings.apply(title)
        return title
    
    def images(self, collectionFile):
        if self.forceDefaultImages:
            return self.defaultIcon, self.defaultThumb
        
        
        collectionFolder = collectionFile.folder
        if collectionFolder.hasSubfolder('_images'):
            imageFolder = collectionFolder.getSubfolder('_images')
            soleName = collectionFile.soleName
            
            if imageFolder.hasFile(soleName + '.png'):
                return imageFolder.getFile(soleName + '.png').fullpath, None    #thumb not used for now
            
            elif imageFolder.hasFile(soleName + '.jpg'):
                return imageFolder.getFile(soleName + '.jpg').fullpath, None    #thumb not used for now
            
            
        return self.defaultIcon, self.defaultThumb