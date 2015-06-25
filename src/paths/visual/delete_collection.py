from src.tools.dialog import dialog
from src.tools.addonSettings import string as st


def confirmDialog(collection):
    HEADING = st(840) 
    LINE1   = st(841)   %collection.title
       
    return dialog.yesno(HEADING, LINE1)



def successDialog(collection):    
    HEADING = st(842)
    LINE1   = st(843)   %collection.title
    
    dialog.ok(HEADING, LINE1)