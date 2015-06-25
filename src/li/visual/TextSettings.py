class TextSettings(object):
    def __init__(self, color, bold, italic, show=True):
        self.color = color
        self.bold = bold
        self.italic = italic
        self.show = show
        
    def apply(self, text):
        if not self.show:
            return ''
        
        
        if self.color is not None:
            text = color(self.color, text)
            
        if self.bold:
            text = bold(text)
            
        if self.italic:
            text = italic(text)
            
        return text


def color(color, text):
    return '[COLOR %s]%s[/COLOR]' %(color, text)

    
def bold(text):
    return '[B]%s[/B]'  %text
    
def italic(text):
    return '[I]%s[/I]'  %text

    
    
    
def fromOther(ts):
    return TextSettings(ts.color, ts.bold, ts.italic, ts.show)