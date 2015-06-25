from src.li.Li import Li

class CustomFileLi(Li):
    def __init__(self, url, customFileVisual):
        
        
        title = customFileVisual.title()
        icon, thumb = customFileVisual.images() 
        
        isFolder = False
        isPlayalbe = False

        generalInfoLabels = None
        videoInfoLabels = None
 
        
        
        super(CustomFileLi, self).__init__(title, icon, thumb, url, isFolder, isPlayalbe,
                                       videoInfoLabels, generalInfoLabels)