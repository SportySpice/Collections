from types import VideoLi
import xbmc
import xbmcgui
from src.paths.root import GENERAL_CACHE_DIR
from src.file import File

PLAYLIST_FILE = 'play_list'


class ItemPlaylist(object):
    def __init__(self):        
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()        
        self.playlist = playlist
        
        self.firstAdded = False
        self.added = 0
    
    def addVideo(self, video, videoVisual, playIfFirst=False, index=-1):
        videoLi = VideoLi.playVideoLi(video, videoVisual)
        
        self.playlist.add(*videoLi.pi, index=index)
                   
        if not self.firstAdded:
            
            if playIfFirst:
                self.play()
                
            self.firstAdded = True
        self.added += 1
        
    def addPi(self, pi):
        self.playlist.add(*pi)
        self.added += 1   
        

        
        

        
        
        
    def addVideoAndResolve(self, video, videoVisual):
        import xbmcplugin
        from src.tools.addonHandle import addonHandle
        
        videoLi = VideoLi.playVideoLi(video, videoVisual)
        li = videoLi.li
                
        self.playlist.add(videoLi.url, li)

        
        #li.setPath(videoLi.url)         
        xbmcplugin.setResolvedUrl(addonHandle, True, li)
        
        
        execStr = 'XBMC.Playlist.PlayOffset({0})'.format(self.added)
        xbmc.executebuiltin(execStr)

                
        
        
           
        if not self.firstAdded:
            self.firstAdded = True
        
        self.added += 1
    
    
    
    def play(self):
        xbmc.Player().play(item=self.playlist)
        
        
    def playFrom(self, position):
        xbmc.Player().play(item=self.playlist, startpos=position)
        
    def playFromLast(self):
        self.playFrom(self.added)
        
        
        

class CacheableVideoLi(object):
    def __init__(self, url, title, thumb, generalInfoLabels, videoInfoLabels):
        self.url = url       
        self.title = title
        self.thumb = thumb                             
        self.generalInfoLabels  = generalInfoLabels
        self.videoInfoLabels    = videoInfoLabels
        


class CachableItemPlaylist(object):
    def __init__(self):
        self.cvls = []
    
    def addItem(self, url, vLi):
        cvl = CacheableVideoLi(url, vLi.title, vLi.thumb, vLi.generalInfoLabels, vLi.videoInfoLabels) 
        self.cvls.append(cvl)        
    
            
    def cache(self): 
        playlistFile = File.fromInvalidNameAndDir(PLAYLIST_FILE, GENERAL_CACHE_DIR)
        playlistFile.dumpObject(self.cvls)   
        
        
        
        
        
def loadFromFile():    
    playlistFile = File.fromInvalidNameAndDir(PLAYLIST_FILE, GENERAL_CACHE_DIR)
    cvls = playlistFile.loadObject()
    playlist = ItemPlaylist()
    
    for cvl in cvls:
        li = xbmcgui.ListItem(cvl.title, thumbnailImage=cvl.thumb)
        
        li.setInfo('general', cvl.generalInfoLabels)
        li.setInfo('video', cvl.videoInfoLabels)
        #li.setProperty('IsPlayable', 'True')
         
        pi = (cvl.url, li)
        playlist.addPi(pi)    
    
    return playlist