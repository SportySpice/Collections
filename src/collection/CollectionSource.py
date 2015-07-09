from settings import globalCollection
from src import router
from src.tools.addonSettings import string as st
from src.tools.enum import enum


OnSourceClick = enum(BROWSE=1, PLAYALL=2, BROWSE_ORIGIN=3)

gfs = None
gss = None
class CollectionSource(object):
    def __init__(self, index, collection, videoSource, onClick=None, limit=None, customTitle=None, customThumb=None):
        self.id = videoSource.id
        self.index = index
        self.collection = collection        
        self.videoSource = videoSource
        
        self._onClick = onClick
        self._limit = limit
        self.customTitle = customTitle
        self.customThumb = customThumb
        
        css = self.collection.sourcesSettings
        self.css = css
        self.csts = css.TS 
        self.cfs = self.collection.feedSettings
        self.cfds = self.collection.folderSettings
        
        
        #methods
        self.isKodiFolder = self.videoSource.isKodiFolder
        self.isChannel = self.videoSource.isChannel
        self.isPlaylist = self.videoSource.isPlaylist
        self.isYoutube = self.videoSource.isYoutube
        
        




    #abstract
    def browseUrl(self):
        pass

    #abstract
    def onClick(self):
        return
        

    
                    
    
    def onClickUrl(self):
        oc = self.onClick()
        if oc == OnSourceClick.BROWSE:
            return self.browseUrl()
    
        elif oc == OnSourceClick.PLAYALL:
            pass
        
        elif oc == OnSourceClick.BROWSE_ORIGIN:
            return self.browseOriginUrl()
        
        else:
            raise ValueError('Unknown onClick value')
    
    
    def limit(self):
        if not self.cfs.useLimits:
            return gfs.sLimit
            
        return self._limit if self._limit else self.cfs.sLimit

    
    
    def title(self):
        if self.customTitle:
            return self.customTitle
        
        return self.videoSource.title
        
        
    def thumb(self):
        if self.customThumb:
            return self.customThumb
        
        return self.videoSource.thumb
    
    
    def liVisuals(self):
        title = self.title()
        title = self.csts.cSourceTS().apply(title)
        
        
        icon  = self.thumb()
        thumb = self.thumb()
            
        
        
        return title, icon, thumb 
    
    
        
    #abstract
    def allVideos(self):
        return
    
    
    def limitedVideos(self):
        allVideos = self.allVideos()
        limit = self.limit()
      
        return allVideos[:limit]
    

    
    
    
    def setOnClick(self, onSourceClick):
        self._onClick = onSourceClick
    
    def setLimit(self, value):
        self._limit = value
        
        
        
    def removeContextMenu(self):
        contextMenu =       (st(410),   'RunPlugin(%s)' % router.removeFromCollectionUrl(self.collection.file, self.id))
        return contextMenu
        
        
    
    
def init():
    global gfs
    gfs = globalCollection.gc().feedSettings        