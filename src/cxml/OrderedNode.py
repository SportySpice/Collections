class OrderedNode(object):
    def __init__(self, name, orderedSettings=None, text=None):
        self.name = name
        self.orderedSettings = orderedSettings
        self.text = text
        
        
        self.children = []
        self.orderedTextRows = [] 
        
        
    def addChild(self, orderedNode):
        self.children.append(orderedNode)
        
    def addChildren(self, children):
        for child in children:
            self.addChild(child)
            
    
    def addTextRow(self, orderedTextRow):
        self.orderedTextRows.append(orderedTextRow)
        
        
    def hasSettings(self):
        if self.orderedSettings and self.orderedSettings.hasValues():
            return True
        
        return False
    
    def hasTextrows(self):
        if self.orderedTextRows:
            return True
        
        return False