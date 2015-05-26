import xbmcplugin
from src.tools.addonHandle import addonHandle
from src.file import Folder
from types.FolderLi import FolderLi
from types.VideoLi import VideoLi
from types.CollectionLi import CollectionLi
from types.SourceListLi import SourceListLi
from types.SourceLi import SourceLi
#import types.FolderLi as FolderLi
#import types.VideoLi as VideoLi
#import types.CollectionLi as CollectionLi





class ItemList(object):
    def __init__(self):
        self.items = []
        
        

    def addFolder(self, folder, folderVisual):                    
        folderLi = FolderLi(folder, folderVisual)
        self.items.append(folderLi.di)
    
    def addFolderfromFP(self, fullpath, folderVisual):
        folder = Folder.fromFullpath(fullpath)
        self.addFolder(folder, folderVisual)
        
    
    
    def addVideo(self, video,videoVisual, special=False, collectionFile=None, sourceSpecial=False, sourceId=None):
        videoLi = VideoLi (video, videoVisual, special, collectionFile, sourceSpecial, sourceId)        
        self.items.append(videoLi.di)
        
    
    def addCollection(self, collectionFile, collectionVisual, shouldPlay=False):
        collectionLi = CollectionLi(collectionFile, collectionVisual, shouldPlay)
        self.items.append(collectionLi.di)
        
        
    def addSourceList(self, collectionFile, sourceListVisual):
        sourceListLi = SourceListLi(collectionFile, sourceListVisual)
        self.items.append(sourceListLi.di)
        
    def addSource(self, source, collectionFile, sourceVisual):
        sourceLi = SourceLi(source, collectionFile, sourceVisual)
        self.items.append (sourceLi.di)
    
        
    def present(self, viewStyle):
        xbmcplugin.setContent(addonHandle, viewStyle)       
        xbmcplugin.addDirectoryItems(addonHandle, self.items, totalItems=len(self.items))
        
        xbmcplugin.endOfDirectory(addonHandle)