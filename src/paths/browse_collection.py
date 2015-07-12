import sort_videolist as svl
from src.collection import Collection
from src.collection.Collection import OnCollectionClick as occ
from src.videosource.VideoList import vsToCounts
from src.li.ItemList import ItemList






def present(collectionFile):
    collection = Collection.fromFile(collectionFile)
      
          
    currentSort = svl.loadCurrentSort()
    selected = currentSort.selected
      
    if selected:
        collection.createCombinedList(customSort=selected, reverse=currentSort.selectedReverse)
        currentSort.setSelectedAsCurrent()
        customVcts = vsToCounts[selected]
    else:
        collection.updateDatedSources()
                
        vs = collection.feedSettings.sort()
        index = vs - 1  #very scatchy use of this enum, change later if causes problems
        reverse = collection.feedSettings.reverseSort()
          
        currentSort.setCurrent(vs, index, reverse)
        customVcts = None
      
      
    fs = collection.feedSettings
    ts = fs.TS
      
    items = ItemList(not fs.playVideoOnly())
      
      
    if collection.onClick() == occ.FEED:
        items.addCollectionSources(collection)
      
    if fs.showSettings() and not (collection.default):
        items.addCollectionSettings(collection)
          
    if fs.showSort():
        items.addVideoSortCollection(collection)
      
    if fs.showPlayAll():    
        items.addCollection(collection, ts.playAllVisual(), onClick=occ.PLAYALL)
          
  
      
      
    videosVisual = ts.videosVisual(customVcts)
    for video in collection.videos:
        items.addVideo(video, videosVisual, collection)            
      
      
    items.present(collection.feedSettings.viewStyle())
    
    
    
    
    
    
    
    
    
    
    
# import xbmcgui
# import xbmc
# from src.videosource.youtube import urlResolver
# from src.videosource.youtube.YoutubeVideo import watchedDic
# from src.tools import videoResolve
# 
# 
# 
# 
#     
#     
# 
# 
# 
# 
# class Window(xbmcgui.WindowXML):
#     def __init__(self, *args, **kwargs):
#         xbmcgui.WindowXMLDialog.__init__( self )
#         self.lis = kwargs['lis']
#     
#     def onInit(self):
#         self.listctrl = self.getControl(52)
#         self.listctrl.addItems(self.lis)
#         
#     def onClick(self, controlID):
#         if (controlID == 52):
#             print '1111111111111111111111111111111'
#             li = self.listctrl.getSelectedItem()
#             videoId = li.getProperty('videoId')
#             url = urlResolver.resolve(videoId)
#             print '22222222222222222222222222222222'
#             watchedDic.videoPlayed(videoId)
#             
#             
#             print 'playing video'
#             xbmc.executebuiltin('XBMC.PlayMedia(%s)' %url)
#             
#             print 'played video'
# 
# 
# 
# 
# 
# 
# def present2(collectionFile):
#     collection = Collection.fromFile(collectionFile)
#     collection.updateDatedSources()
#     
#     lis = []
#     for video in collection.videos:
#         li = xbmcgui.ListItem(video.title, iconImage=video.thumb, thumbnailImage=video.thumb)
#         li.setProperty('sourceTitle', video.source.title)
#         li.setProperty('viewCount', str(video.viewCount))
#         li.setProperty('videoId', str(video.id))
#         
#         lis.append(li)
#         
#     
#     window = Window('vloody.xml', 'C:\\Users\Vlood\\AppData\Roaming\\Kodi\\addons\\plugin.video.collections', lis=lis)
#     #list = window.getControl(51)
#     #list.additem(li)
#     
#     #window.addItem(li, position=1)
#     
#     
#     window.doModal()