import xbmcgui

#abstract
class Li(object):
    def __init__(self, title, icon, thumb, url, isFolder, isPlayalbe, 
                 videoInfoLabels, generalInfoLabels):    
              
        li = xbmcgui.ListItem (title, iconImage=icon, thumbnailImage=thumb)
        
        if isPlayalbe:
            li.setProperty('IsPlayable', 'True')
                
        
        
        if generalInfoLabels is not None:
            li.setInfo('general', generalInfoLabels)
        if videoInfoLabels is not None:
            li.setInfo('video', videoInfoLabels)
            
                
        self.li = li
        self.di = (url, li, isFolder)
        self.url = url