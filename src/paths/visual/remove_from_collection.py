from src.tools.dialog import dialog
from src.tools.addonSettings import string as st


def confirmDialog(cSource, collection):
    HEADING = st(830) 
    LINE1   = st(831)   %(cSource.typeText(), cSource.title(), collection.title)
       
    return dialog.yesno(HEADING, LINE1)



def successDialog(cSource, collection):    
    HEADING = st(832)
    LINE1   = st(833) %(cSource.typeText(), cSource.title(), collection.title)
    
    dialog.ok(HEADING, LINE1)