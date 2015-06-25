class OrderedTextRow(object):
    def __init__(self, text, orderedSettings, comment=None):
        self.text = text
        self.orderedSettings = orderedSettings
        self.comment = comment
        
        
    def hasSettings(self):
        if self.orderedSettings and self.orderedSettings.hasValues():
            return True
        
        return False
    
    def hasComment(self):
        if self.comment:
            return True
        
        return False