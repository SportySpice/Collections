import xbmc

kb = xbmc.Keyboard()

def show(heading, default=None):
    if default:
        kb.setDefault(default)
        
    kb.setHeading(heading)
    kb.doModal()
    
    
def gotInput():
    if kb.isConfirmed():
        return True
    
def text():
    return kb.getText()