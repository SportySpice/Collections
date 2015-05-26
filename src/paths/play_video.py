import xbmcgui
import xbmcplugin
from src.tools.addonHandle import addonHandle
from src.youtube import urlResolver
from src.tools import watchedDic




def play(videoId):        
    streamurl = urlResolver.resolve(videoId)
    listItem = xbmcgui.ListItem("", path=streamurl)     
    xbmcplugin.setResolvedUrl(addonHandle, True, listItem)
    
    
    watchedDic.videoPlayed(videoId)