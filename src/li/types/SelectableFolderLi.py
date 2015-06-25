from src.li.Li import Li
from src import router

class SelectableFolderLi(Li):
    def __init__(self, folder, folderVisual, relativePath=None):
        
        
        title = folderVisual.title(folder)
        icon, thumb = folderVisual.images(folder) 
        
        url = router.addToCollectionBrowseUrl(relativePath)
        
        isFolder = True
        isPlayalbe = False

        generalInfoLabels = None
        videoInfoLabels = None
 
        
        
        super(SelectableFolderLi, self).__init__(title, icon, thumb, url, isFolder, isPlayalbe,
                                       videoInfoLabels, generalInfoLabels)