from visual.browse_kodi_folder import viewStyle, addToCollectionVisual, foldersVisual, videosVisual
from src.li.ItemList import ItemList
from src.videosource.kodi import KodiFolder
from src.tools import dialog
from src.tools.addonSettings import string as st

def browse(kodiFolderFile, rootFolder=False):
    kodiFolder = KodiFolder.fromCacheFile(kodiFolderFile)
    folders, videos, allItems = kodiFolder.updatedContents()
    
    if kodiFolder.updateFailed():
        dialog.ok(  st(760), st(761), st(762)   )       #parse error dialog
        return
    
    
    
    
    items = ItemList()
        
    if kodiFolder.isEmpty():
        items.present(viewStyle)
        return
    
    
    
    
    if videos and not rootFolder:
        items.addAddToCollection(kodiFolder, addToCollectionVisual)
    
    if rootFolder:
        for folder in folders:
            if folder.path != 'plugin://plugin.video.collections':
                items.addKodiFolder(folder, foldersVisual)
    
    else:


        for folder in folders:
            items.addKodiFolder(folder, foldersVisual)
        
        for kodiVideo in videos:
            #items.addKodiVideo(kodiVideo, videosVisual)
            items.addVideoPlay(kodiVideo, videosVisual)
        
    items.present(viewStyle)