import sort_videolist as svl
from visual.browse_kodi_folder import viewStyle, addToCollectionVisual, foldersVisual, videosVisual
from src.li.ItemList import ItemList
from src.videosource.kodi import KodiFolder
from src.tools import dialog
from src.tools.addonSettings import string as st
from src.videosource.VideoList import VideoSort as vsr, vsToCounts


VIDEO_SORT_OPTIONS  = (vsr.DATE,    vsr.DURATION,  vsr.SHUFFLE,    vsr.VIDEO_TITLE,         vsr.PLAYCOUNT,  vsr.LASTPLAYED)
VIDEO_SORT_LABELS   = (st(620),     st(622),       st(624),        st(627),                 st(632),        st(633)       )


def browse(kodiFolderFile, rootFolder=False):
    kodiFolder = KodiFolder.fromCacheFile(kodiFolderFile)
    folders, videos, allItems = kodiFolder.updatedContents()
    
    if kodiFolder.updateFailed():
        dialog.ok(  st(760), st(761), st(762)   )       #parse error dialog
        return
    
    
    
    
    items = ItemList(hasQeuingVideos=True)
        
    if kodiFolder.isEmpty():
        items.present(viewStyle)
        return
    
    
    

    
    
        
    
    if rootFolder:
        for folder in folders:
            if not folder.path.startswith('plugin://plugin.video.collections'):                
                items.addKodiFolder(folder, foldersVisual)
    
    else:
        if videos:
            items.addAddToCollection(kodiFolder, addToCollectionVisual)
            
            items.addVideoSortKodi(st(751))                
            currentSort = svl.loadCurrentSort()
            selected = currentSort.selected
            
            if selected:
                videos.sort(selected, reverseOrder=currentSort.selectedReverse)   #might cause problems in future cause
                currentSort.setSelectedAsCurrent()                                               #didn't make a copy
                customVcts = vsToCounts[selected]
                videosVisual.setCustomVcts(customVcts)                
            else:           
                currentSort.setCurrent(vsr.DATE, 0, False)
            

        for folder in folders:
            items.addKodiFolder(folder, foldersVisual)
        
        for kodiVideo in videos:
            #items.addKodiVideo(kodiVideo, videosVisual)
            items.addVideo(kodiVideo, videosVisual)
        
    items.present(viewStyle)