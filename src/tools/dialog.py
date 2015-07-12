import xbmcgui
from src.tools.enum import enum
dialog = xbmcgui.Dialog()


def ok(heading, line1, line2=None, line3=None):
    return dialog.ok(heading, line1, line2, line3)
    
    
def select(heading, stringList, autoclose=0):
    return dialog.select(heading, stringList, autoclose)




BrowseType = enum (SHOW_AND_GET_DIR=0, SHOW_AND_GET_FILE=1, SHOW_AND_GET_IMAGE=2, 
                   SHOW_AND_GET_WRITEABLE_DIR=3)

def browse(browseType, heading, s_shares, mask=None, useThumbs=False, treatAsFolder=False, default=None, 
           enableMultiple=False):
    return dialog.browse(browseType, heading, s_shares, mask, useThumbs, treatAsFolder, default, enableMultiple)


# def input(heading, default=None, type=None, option=0, autoclose=None):
#     return dialog.input(heading, default, xbmcgui.INPUT_ALPHANUM, option)
    #return dialog.input(heading)
    

# def notification(heading, message, icon=None, time=None, sound=None):
#     dialog.notification(heading, message, icon=icon, time=15, sound=sound)
    
    
   
    
    