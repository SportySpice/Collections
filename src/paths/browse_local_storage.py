import sys
import string
from src.li.ItemList import ItemList
from visual.browse_local_storage import viewStyle, drivesVisual
from src.videosource.kodi import KodiFolder 

def browse():
    if 'win' not in sys.platform:
        raise ValueError('Only windows is supported for browsing local storage at this time')

    items = ItemList()
    
    for drive in _getDrives():        
        path = drive + ':\\'
        title = path 
        thumb = None
        kodiFolder = KodiFolder.fromPath(path, title, thumb)
        
        items.addKodiFolder(kodiFolder, drivesVisual)
        
    items.present(viewStyle)
        
        
        
        
def _getDrives():
    from ctypes import windll
    
    
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()  # @UndefinedVariable
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives