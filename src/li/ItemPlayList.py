from types import VideoLi
import xbmc

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