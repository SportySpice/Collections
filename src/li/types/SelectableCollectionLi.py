from src.li.Li import Li

class SelectableCollectionLi(Li):
    def __init__(self, collection, collectionVisual):
        title = collectionVisual.title(collection)
        
        icon, thumb = collectionVisual.images(collection)
        
        url = collection.file.fullpath
        
        isFolder = False
        isPlayalbe = False
            
        generalInfoLabels = None
        videoInfoLabels = None
 
    
        super(SelectableCollectionLi, self).__init__(title, icon, thumb, url, isFolder, isPlayalbe,
                                       videoInfoLabels, generalInfoLabels)