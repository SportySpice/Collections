from src.gui.SettingsWindow import SettingsWindow
from src.gui.Tab import Tab
import xbmc

from src.videosource.youtube.Subscriptions import SubscriptionSorting as ss

SORTING_OPTIONS   = [ss.ALPHABETICAL,   ss.RELEVANCE,   ss.UNREAD]
SORTING_LABELS    = ['Alphabetical',    'Relevance',    'Unread']


def edit():
    window = SettingsWindow('Subscriptions Settings', saveCallback=None, hideTabs=True)
    
    generalTab = Tab('General')
    generalTab.addEmptyRow()
    
    generalTab.addEnum('Sorting', SORTING_OPTIONS, ss.ALPHABETICAL, ss.ALPHABETICAL, lambda value: value, customLabels=SORTING_LABELS)
    
    window.addTabs([generalTab])
    
    
    xbmc.executebuiltin('XBMC.Dialog.Close(all, true)')
    window.show()
    window.delete()