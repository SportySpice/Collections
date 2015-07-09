from root import GENERAL_CACHE_DIR
from src.file import File
from src.tools.dialog import dialog
from src.tools import xbmcTool
from src.li.visual import TextSettings as ts
from src.tools.addonSettings import string as st
from src.videosource.VideoSource import SourceType



def sort(sourceType=None):
    currentSort = loadCurrentSort(sourceType)
                
    if sourceType is None:                  from edit_collection        import VIDEO_SORT_OPTIONS, VIDEO_SORT_LABELS        
    elif sourceType == SourceType.FOLDER:   from browse_kodi_folder     import VIDEO_SORT_OPTIONS, VIDEO_SORT_LABELS
    else:                                   from browse_youtube_channel import VIDEO_SORT_OPTIONS, VIDEO_SORT_LABELS                                                                           
            
    
    labels = list(VIDEO_SORT_LABELS)    #copy list
    
#     if currentSort.current == VideoSort.SHUFFLE:
#         arrow = '*'
#     else:
#         arrow = '^'  if currentSort.currentReverse else 'v'
        
    arrow = ' *'
    labels[currentSort.currentIndex] += ts.color('red', arrow)
    
    index = dialog.select(st(432), labels)
    if index == -1:
        return
    
    currentSort.setSelected(VIDEO_SORT_OPTIONS[index], index)
    xbmcTool.refreshContainer()
    


    
    
    
    

FEED_SORT_FILE      ='current_feed_sort'
KODI_SORT_FILE      ='current_kodi_sort'
YOUTUBE_SORT_FILE   ='current_youtube_sort'


class CurrentSort(object):
    def __init__(self, sortFile):
        self.sortFile = sortFile
                
        self.current            = None
        self.currentReverse     = None
        self.currentIndex       = None
        
        self.selected           = None
        self.selectedReverse    = None
        self.selectedIndex      = None
        
    
    def setCurrent(self, vs, index, reverse):
        self.current        = vs
        self.currentIndex   = index
        self.currentReverse = reverse
        
        self.selected       = None
        self.selectedIndex  = None
        self.selectedReverse= None
        self.cache()
    
    
    def setSelectedAsCurrent(self):
        self.setCurrent(self.selected, self.selectedIndex, self.selectedReverse)
        
    def setSelected(self, selected, index, reverse=False, reverseIfSame=True):
        self.selected       = selected
        self.selectedIndex  = index
        
        if (reverseIfSame) and index == self.currentIndex:
            self.selectedReverse = not self.currentReverse
        else:
            self.selectedReverse = reverse
        
        
        self.cache()
        
    
        
        
    def cache(self):
        self.sortFile.dumpObject(self)
    
    


def loadCurrentSort(sourceType=None):
    if sourceType is None:                      sortFile = FEED_SORT_FILE
    elif sourceType == SourceType.FOLDER:       sortFile = KODI_SORT_FILE
    else:                                       sortFile = YOUTUBE_SORT_FILE                                                                       
    
    sortFile = File.fromNameAndDir(sortFile, GENERAL_CACHE_DIR)
        
    if sortFile.exists():        
        currentSort = sortFile.loadObject()
        return currentSort
    else:
        return CurrentSort(sortFile)











#from src.collection.xml.strings import vsrToValue
#vsStr = vsrToValue[vs]

#from src.collection.xml.strings import valueTovsr
#vsStr = selectedSortFile.loadObject()
#vs = valueTovsr[vsStr]



# from src.gui.SettingsWindow import SettingsWindow
# from src.gui.Tab import Tab
# def edit():    
#     window = SettingsWindow('Sort By', width=500, height=600, hideTabs=True, showButtons=False)
#     currentSort = loadCurrentSort()
#     
#     window.addCustomButton('lol', 2, lambda value:value)
#     window.addCustomButton('boo', 4, lambda value:value)
#     window.addCustomButton('fish', 6, lambda value:value)
#     window.placeCustomButtons()
#     
#     tab = Tab('', rows=15)
#     
#     
#      
#     def onClick(button, index):
#         vs = VIDEO_SORT_OPTIONS[index]        
#         currentSort.setSelected(vs)        
#                        
#         xbmcTool.refreshContainer()        
#         button.control.setLabel('hmm')
#      
#     for i in range(len(VIDEO_SORT_OPTIONS)):            
#         label = VIDEO_SORT_LABELS[i]
#         vs = VIDEO_SORT_OPTIONS[i]
#         
#         if vs == currentSort.current:
#             label = label + '(current)'
#         
#         button = tab.addButton(label, None, columnSpan=8, centered=False)
#         button.action = lambda button=button, index=i: onClick(button, index)
#          
#     window.addTabs([tab])
#      
#     window.show()
#     window.delete()      
        
    
#from src.tools.dialog import dialog   
#     selectedSortFile = File.fromNameAndDir(SELECTED_SORT_FILE, GENERAL_CACHE_DIR)
#     vs = VIDEO_SORT_OPTIONS[result]
#     vsStr = vsrToValue[vs]
#     
#     selectedSortFile.dumpObject(vsStr)
#     xbmcTool.refreshContainer()