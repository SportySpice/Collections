import xbmcgui

#abstract
class Li(object):
    def __init__(self, title, icon, thumb, url, isFolder, isPlayalbe, 
                 videoInfoLabels, generalInfoLabels, contextMenus=None):    
              
        li = xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=thumb)
        
        if isPlayalbe:
            li.setProperty('IsPlayable', 'True')
                
        
        
        if generalInfoLabels is not None:
            li.setInfo('general', generalInfoLabels)
        if videoInfoLabels is not None:
            li.setInfo('video', videoInfoLabels)
            
                
        self.li = li
        self.di = (url, li, isFolder)
        self.url = url
        
        
        if contextMenus:
            li.addContextMenuItems(contextMenus)
            
            
            
            
def runPluginCm(label, url):
    return ('%s' %label, 'RunPlugin(%s)' %url)