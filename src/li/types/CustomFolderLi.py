from src.li.Li import Li

class CustomFolderLi(Li):
    def __init__(self, url, customFolderVisual):
        
        
        title = customFolderVisual.title()
        icon, thumb = customFolderVisual.images() 
        
        isFolder = True
        isPlayalbe = False

        generalInfoLabels = None
        videoInfoLabels = None
 
        
        
        super(CustomFolderLi, self).__init__(title, icon, thumb, url, isFolder, isPlayalbe,
                                       videoInfoLabels, generalInfoLabels)