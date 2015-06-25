from src.tools.dialog import dialog
from src.tools import dialogProgress
from src.tools.addonSettings import string as st

                      
def signInDialog():
    HEADING =   st(850)
    OPTIONS = ( st(851), st(852)    )
    
    return dialog.select(HEADING, OPTIONS)




def codeDialog(code):
    HEADING =   st(855)
    LINE1 =     st(856)
    LINE2 =     st(857) %code
    
    dialogProgress.create(HEADING, LINE1, LINE2)
    return dialogProgress



    
    
def signOutDialog():
    HEADING = st(860)
    LINE1   = st(861) 
    
    return dialog.yesno(HEADING, LINE1)






def signInSuccessDialog():
    HEADING = st(865)
    LINE1   = st(866)
    
    dialog.ok(HEADING, LINE1)

def signOutSuccessDialog():
    HEADING = st(865)
    LINE1   = st(867)
    
    dialog.ok(HEADING, LINE1)   