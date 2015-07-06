import xbmc


def refreshContainer():
    xbmc.executebuiltin('XBMC.Container.Refresh()')
    

def closeOpenDialogs():
    xbmc.executebuiltin('XBMC.Dialog.Close(all, true)')