from src.tools import dialog
from src.tools.addonSettings import string as st



BROWSE_DIALOG_HEADING = st(810)

def alreadyInCollectionDialog(vSource, collection):
    HEADING       =   st(811)
    LINE1         =   st(812)    %(vSource.typeText(), vSource.title, collection.title)
    
    dialog.ok(HEADING, LINE1)


def successDialog(vSource, collection):    
    HEADING       =   st(813)
    LINE1         =   st(814)    %(vSource.typeText(), vSource.title, collection.title)
    
    dialog.ok(HEADING, LINE1)