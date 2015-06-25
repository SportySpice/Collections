from src.tools.dialog import dialog
from src.tools.addonSettings import string as st

def successDialog():
    HEADING = st(870)
    LINE1   = st(871)
    
    dialog.ok(HEADING, LINE1)
    