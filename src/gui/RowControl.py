import pyxbmct.addonwindow as pyxbmct

class RowControl(object):
    def __init__(self, control, column, columnspan=1, padX=0, action=None, onDefault=None, onSave=None, init=None, rowspan=1, enabled=True):
        self.control = control
        self.column = column
        self.columnspan = columnspan
        self.padX = padX
        self.action = action
        self.onDefault = onDefault
        self.onSave = onSave        
        self.rowspan = rowspan
        
        
        if type(control) is pyxbmct.List:
            self.isList = True
        else:
            self.isList = False
            
        
        self.visible = True
        self.enabled = enabled
        self.globalEnabled = True
        
        
        
        if enabled:
            self.init = init
        else:
            self._init = init
    
    
    def init(self):
        self.updateState()
        if self._init:
            self._init()
                
            
    
        
        
    def updateState(self):
        if self.isList:
            self.control.setEnabled(self.enabled)
            
            if self.visible and self.globalEnabled:
                self.control.setVisible(True)                    
            else:
                self.control.setVisible(False)
                
            
                    
        
        else:
            if self.enabled and self.globalEnabled:
                self.control.setEnabled(True)
                
            else:
                self.control.setEnabled(False)
            
    
    
    def setVisible(self, state):
        self.visible = state
        
        if self.isList:        
            self.updateState()            
            
        else:            
            self.control.setVisible(state)
        
        
    def setEnabled(self, state):
        self.enabled = state
        self.updateState()
        
        
        
    def setGlobalEnabled(self, state):
        self.globalEnabled = state
        self.updateState()