from src.tools.dialog import dialog
from src.tools.addonSettings import string as st


def noVideosDialog(kodiFolder):
    HEADING = st(810)
    LINE1   = st(811) %len(kodiFolder.folders())
    LINE2   = st(812) 
    OPTIONS = [
        st(813),
        st(814)
    ]
    if dialog.ok(HEADING, LINE1, LINE2):
        return dialog.select(HEADING, OPTIONS)
    
    return -1

def customTitleDialog(kodiFolder):    
    HEADING = st(815)
    return dialog.input(HEADING, kodiFolder.title)
    
    


BROWSE_DIALOG_HEADING = st(816)

def alreadyInCollectionDialog(vSource, collection):
    HEADING       =   st(817)
    LINE1         =   st(818)    %(vSource.typeText(), vSource.title, collection.title)
    
    dialog.ok(HEADING, LINE1)


def successDialog(cSource, collection):    
    HEADING       =   st(819)
    LINE1         =   st(820)    %(cSource.typeText(), cSource.title(), collection.title)
    
    dialog.ok(HEADING, LINE1)