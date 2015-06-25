import xbmcgui

dialogProgress = xbmcgui.DialogProgress()



def create(heading, line1=None, line2=None, line3=None):
    dialogProgress.create(heading, line1, line2, line3)
    
def iscanceled():
    return dialogProgress.iscanceled()
    
def close():
    dialogProgress.close()