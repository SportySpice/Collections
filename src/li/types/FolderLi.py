from src.li.Li import Li
from src import router

class FolderLi(Li):
    def __init__(self, folder, folderVisual):
        
        
        title = folderVisual.title(folder)
        icon, thumb = folderVisual.images(folder) 
        
        url = router.browseFolderUrl(folder)
        
        isFolder = True
        isPlayalbe = False

        generalInfoLabels = None
        videoInfoLabels = None
 
        
        
        super(FolderLi, self).__init__(title, icon, thumb, url, isFolder, isPlayalbe,
                                       videoInfoLabels, generalInfoLabels)