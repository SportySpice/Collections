class Node(object):
    def __init__(self, name, settings, text):
        self.name = name
        self.settings = settings
        self.text = text
        
        self.textRows = [] 
        
        
        
    def addTextRow(self, textRow):
        self.textRows.append(textRow)
        
        
        
        
def empty(name):
    return Node(name, {}, '')