class TextSettings:
    def __init__(self, color, bold, italic):
        self.color = color
        self.bold = bold
        self.italic = italic
        
    def apply(self, text):
        if self.color is not None:
            text = '[COLOR %s]%s[/COLOR]' %(self.color, text)
            
        if self.bold:
            text = '[B]%s[/B]' %text
            
        if self.italic:
            text = '[I]%s[/I]' %text
            
        return text