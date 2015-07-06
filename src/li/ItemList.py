from ItemPlayList import CachableItemPlaylist
import xbmcplugin
from src.tools.addonHandle import addonHandle
from src.file import Folder
from types.FolderLi import FolderLi
from types import VideoLi
from types.CollectionLi import CollectionLi
from types.CollectionSourcesLi import CollectionSourcesLi
from types.CollectionSourceLi import CollectionSourceLi
from types.CustomFolderLi import CustomFolderLi
from types.KodiFolderLi import KodiFolderLi
from src.li.types.KodiVideoLi import KodiVideoLi
from types.YoutubeCategoryLi import YoutubeCategoryLi
from types.YoutubeChannelLi import YoutubeChannelLi
from types.YoutubeChannelPlaylistsLi import YoutubeChannelPlaylistsLi
from types.YoutubePlaylistLi import YoutubePlaylistLi
from types.AddToCollectionLi import AddToCollectionLi
from types.SelectableFolderLi import SelectableFolderLi
from types.SelectableCollectionLi import SelectableCollectionLi
from types.CustomFileLi import CustomFileLi
from types.CollectionSettingsLi import CollectionSettingsLi
from types import VideoSortLi
#import types.FolderLi as FolderLi
#import types.VideoLi as VideoLi
#import types.CollectionLi as CollectionLi





class ItemList(object):
    def __init__(self, hasQeuingVideos=False):
        self.items = []
        
        
        self.hasQueingVideos = hasQeuingVideos
        if hasQeuingVideos:
            self.playlist = CachableItemPlaylist()
            self.numVideos = 0
            
        
        
            
            
            
    
        
        

    def addFolder(self, folder, folderVisual):                    
        folderLi = FolderLi(folder, folderVisual)
        self.items.append(folderLi.di)
    
    def addFolderfromFP(self, fullpath, folderVisual):
        folder = Folder.fromFullpath(fullpath)
        self.addFolder(folder, folderVisual)
        
    
    
        
            
        
    def addVideo(self, video, videoVisual, collection=None):
        if self.hasQueingVideos:
            videoLi = VideoLi.queuePlaylistLi(video, self.numVideos, videoVisual, collection)
        
            self.items.append(videoLi.di)            
            self.playlist.addItem(video.playUrl(), videoLi)
        
            self.numVideos += 1
            
        else:
            videoLi = VideoLi.playVideoLi(video, videoVisual, collection)        
            self.items.append(videoLi.di)
        
        
#     def addVideoQueueCollection(self, video, collection, videoVisual):
#         videoLi = VideoLi.queueCollectionLi(video, collection, videoVisual)
#         self.items.append(videoLi.di)
        
        
        
        
    def addCollection(self, collection, collectionVisual, onClick=None, deleteContext=False):
        collectionLi = CollectionLi(collection, collectionVisual, onClick, deleteContext)
        self.items.append(collectionLi.di)
        
        
    def addCollectionSources(self, collection):
        collectionSourcesLi = CollectionSourcesLi(collection)
        self.items.append(collectionSourcesLi.di)
        
    def addCollectionSource(self, cSource):
        cSourceLi = CollectionSourceLi(cSource)
        self.items.append (cSourceLi.di)
        
    
    def addCustomFolder(self, url, customFolderVisual):
        customFolderLi = CustomFolderLi(url, customFolderVisual)
        self.items.append(customFolderLi.di)
    
    
    def addKodiFolder(self, kodiFolder, kodiFolderVisual, root=False):
        kodiFolderLi = KodiFolderLi(kodiFolder, kodiFolderVisual, root)
        self.items.append(kodiFolderLi.di)
        
    def addKodiVideo(self, kodiVideo, kodiVideoVisual):
        kodiVideoLi = KodiVideoLi(kodiVideo, kodiVideoVisual)
        self.items.append(kodiVideoLi.di)
        
        
    
    def addYoutubeCategory(self, category, youtubeCategoryVisual, pageNum=1):
        youtubeCategoryLi = YoutubeCategoryLi(category, youtubeCategoryVisual, pageNum)
        self.items.append(youtubeCategoryLi.di)
        
        
    def addYoutubeChannel(self, channel, youtubeChannelVisual, pageNum=1):
        youtubeChannelLi = YoutubeChannelLi(channel, youtubeChannelVisual, pageNum)
        self.items.append(youtubeChannelLi.di)
        
    def addYoutubeChannelPlaylists(self, channel, youtubeChannelPlaylistsVisual, pageNum=1):
        youtubeChannelPlaylistsLi = YoutubeChannelPlaylistsLi(channel, youtubeChannelPlaylistsVisual, pageNum)
        self.items.append(youtubeChannelPlaylistsLi.di)
        
    def addYoutubePlaylist(self, playlist, youtubePlaylistVisual, pageNum=1):
        youtubePlaylistLi = YoutubePlaylistLi(playlist, youtubePlaylistVisual, pageNum)
        self.items.append(youtubePlaylistLi.di)
        
        
    def addAddToCollection(self, vSource, addToCollectionVisual):
        addToCollectionLi = AddToCollectionLi(vSource, addToCollectionVisual)
        self.items.append(addToCollectionLi.di)
        
    def addSelectableFolder(self, folder, folderVisual, relativePath=None):
        selectableFolderLi = SelectableFolderLi(folder, folderVisual, relativePath)
        self.items.append(selectableFolderLi.di)
        
    def addSelectableCollection(self, collection, collectionVisual):
        selectableCollectionLi = SelectableCollectionLi(collection, collectionVisual)
        self.items.append(selectableCollectionLi.di) 
        
    def addCustomFile(self, url, customFileVisual):
        customFileLi = CustomFileLi(url, customFileVisual)
        self.items.append(customFileLi.di)
        
        
    def addCollectionSettings(self, collection=None):
        collectionSettingsLi = CollectionSettingsLi(collection)
        self.items.append(collectionSettingsLi.di)
        
    def addVideoSortCollection(self, collection):
        videoSortLi = VideoSortLi.collectionVideoSortLi(collection)
        self.items.append(videoSortLi.di)
        
    def addVideoSortYoutube(self, title):
        videoSortLi = VideoSortLi.youtubeVideoSortLi(title)
        self.items.append(videoSortLi.di)
        
    def addVideoSortKodi(self, title):
        videoSortLi = VideoSortLi.kodiVideoSortLi(title)
        self.items.append(videoSortLi.di)
        
        
    def present(self, viewStyle):        
        xbmcplugin.setContent(addonHandle, viewStyle)
        xbmcplugin.addDirectoryItems(addonHandle, self.items, totalItems=len(self.items))
        
        
#         xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_LISTENERS)         
#         
        #xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_DATE)
        #xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_DATEADDED)
        #xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        #xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_STUDIO)
#         #xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_TITLE)
#         #xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_LABEL)
#         xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_EPISODE)
#         
#         xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_VIDEO_RATING)
#         
#         xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_DURATION)
#         
#         xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_LASTPLAYED)
#         xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_PLAYCOUNT)
# 
#         
#         xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_NONE)
#         xbmcplugin.addSortMethod(addonHandle, xbmcplugin.SORT_METHOD_UNSORTED)
        
        
        xbmcplugin.endOfDirectory(addonHandle)
        
        if self.hasQueingVideos:
            self.playlist.cache()