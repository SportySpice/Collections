from src.li.Li import Li
from src import router

class YoutubeCategoryLi(Li):
    def __init__(self, category, youtubeCategoryVisual, pageNum=1):
        title = youtubeCategoryVisual.title(category, pageNum)   
        
        icon = None
        thumb = None
        
        url = router.browseYoutubeCategoryUrl(category.cacheFile, pageNum)
        
        isFolder = True
        isPlayable = False
            
        generalInfoLabels = None
        videoInfoLabels = None
 
    
        super(YoutubeCategoryLi, self).__init__(title, icon, thumb, url, isFolder, isPlayable,
                                       videoInfoLabels, generalInfoLabels)