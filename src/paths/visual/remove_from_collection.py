from src.tools.dialog import dialog
from src.tools.addonSettings import string as st


def confirmDialog(vSource, collection):
    HEADING = st(830) 
    LINE1   = st(831)   %(vSource.typeText(), vSource.title, collection.title)
       
    return dialog.yesno(HEADING, LINE1)



def successDialog(vSource, collection):    
    HEADING = st(832)
    LINE1   = st(833) %(vSource.typeText(), vSource.title, collection.title)
    
    dialog.ok(HEADING, LINE1)