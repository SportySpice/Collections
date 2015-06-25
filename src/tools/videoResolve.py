import xbmcgui
import xbmcplugin
from src.tools.addonHandle import addonHandle

def resolve(url):
    listItem = xbmcgui.ListItem("", path=url)     
    xbmcplugin.setResolvedUrl(addonHandle, True, listItem)