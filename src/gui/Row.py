from RowControl import RowControl
import pyxbmct.addonwindow as pyxbmct
from EnumButton import EnumButton, EnumMode
from src.li.visual import TextSettings as ts
from src.tools.dialog import dialog
import xbmcgui






class Row(object):
    def __init__(self):
        self.rowControls = []
    
    def addRowControl(self, control, column, columnspan=1, padX=0, action=None, onDefault=None, onSave=None, init=None, rowspan=1, enabled=True):
        rowControl = RowControl(control, column, columnspan, padX, action, onDefault, onSave, init, rowspan, enabled)
        self.rowControls.append(rowControl)
        
        return rowControl
        
        
        
    def addLabel(self, label, column, columnspan=1, padX=0, alignment=None, bold=False):
        if bold:
            label = ts.bold(label)
        
        if alignment is not None:
            labelC = pyxbmct.Label(label, alignment=alignment)
        else:
            labelC = pyxbmct.Label(label)
            
        
            
        rowControl = self.addRowControl(labelC, column, columnspan, padX)        
        return rowControl
      
      
    def addTextBox(self, column, columnspan=1, padX=0, rowspan=2):                                
        textBox = pyxbmct.TextBox(font='font4')                                        
        rowControl = self.addRowControl(textBox, column, columnspan, padX, rowspan=rowspan)
                
                
        return rowControl
    
    
    def addList(self, items, column, space=10, textOffsetX=0, columnspan=1, padX=0, rowspan=2, enabled=False):                                
        listC = pyxbmct.List(_space=space, _itemTextXOffset=textOffsetX)
        
        def init():
            for item in items:
                listC.addItem(item)
                
        
        rowControl = self.addRowControl(listC, column, columnspan, padX, rowspan=rowspan, init=init, enabled=enabled)
                
        return rowControl
      
        
        
    def addButton(self, label, column, onClick, columnspan=1, padX=0, alignment=None, bold=False):
        if bold:
            label = ts.bold(label)                
        button = _createButton(label, alignment)
        
        self.addRowControl(button, column, columnspan, padX, action=onClick)
        
        
        
        
        
    def addEnumButton(self, label, values, current, default, column, saveCallback=None, changeCallback=None, customLabels=None, mode=EnumMode.SELECT, returnValue=False, alignment=None, columnspan=1, padX=0, enabled=True):
        enumButton = EnumButton(label, values, current, default, changeCallback, saveCallback, customLabels, mode, returnValue, alignment)        
        rowControl = self.addRowControl(enumButton.button, column, columnspan, padX, action=enumButton.onClick, onDefault=enumButton.onDefault, onSave=enumButton.onSave, enabled=enabled)
        
        return rowControl

    
    


    def addRadioButton(self, column, current, default, saveCallback=None, changeCallback=None, label='', columnspan=1, padX=0, textOffsetX=0, alignment=None, enabled=True):
        if alignment is not None:    
            radioB = pyxbmct.RadioButton(label, _alignment=alignment, textOffsetX=textOffsetX)
        else:                        
            radioB = pyxbmct.RadioButton(label, textOffsetX=textOffsetX)
            
        assignedValue = [False]     #this is a list only cause of python scope issues
        
        
        def init():
            radioB.setSelected(current)
            
        def onChange():
            assignedValue[0] = [True]
            if changeCallback:
                changeCallback(bool(radioB.isSelected()))
        
        def onDefault():
            radioB.setSelected(default)
            onChange()
        
        if saveCallback:            
            def onSave():
                if assignedValue[0]:
                    saveCallback(bool(radioB.isSelected()))
        else:
            onSave = None
 
 
        rowControl = self.addRowControl(radioB, column, columnspan, padX, action=onChange, onDefault=onDefault, onSave=onSave, init=init, enabled=enabled)        
        return rowControl
        
        
    def addInputEdit(self, label, column, current, default, saveCallback, columnspan=1, padX=0):
        editB = pyxbmct.Edit('') 
        
        def init():
            editB.setText(current)
        
        def onDefault():
            editB.setText(default)
            
        def onSave():
            value = editB.getText()
            if value != current:
                saveCallback(value)

                             
                             
        self.addRowControl(editB, column, columnspan, padX, onDefault=onDefault, onSave=onSave, init=init)
        
        
        
        
        
        
    def addInputButton(self, label, column, current, default, saveCallback, changeCallback=None, inputType=xbmcgui.INPUT_ALPHANUM, alignment=None, columnspan=1, padX=0):            
        assignedValue = [False]     #this is a list only cause of python scope issues
        button = _createButton(str(current), alignment)
            
        def buttonAction():
            currentValue = button.getLabel()
            userInput = dialog.input(label, currentValue, type=inputType)
            
            if userInput == '':
                return
            
            asign(userInput)
            
       
        def onDefault():
            asign(str(default))
              
        def onSave():
            if assignedValue[0]:                
                saveCallback(getValue())
        
        
        def asign(value):
            button.setLabel(value)
            assignedValue[0] = True
            
            if changeCallback:
                changeCallback(getValue())
                
        
        def getValue():
            value = button.getLabel()
            if inputType == xbmcgui.INPUT_NUMERIC:
                value = int(value)
                
            return value
                               
                               
        self.addRowControl(button, column, columnspan, padX, action=buttonAction, onDefault=onDefault, onSave=onSave)
        


    
    
    


    def setVisible(self, state):
        for rowControl in self.rowControls:
            rowControl.setVisible(state)
            
        
    def hide(self):
        self.setVisible(False)
        
                        
    def unHide(self):
        self.setVisible(True)
        
        
        
        
    
    def setEnabled(self, state):   
        for rowControl in self.rowControls:
            rowControl.setEnabled(state)
            
    def enable(self):
        self.setEnabled(True)
        
                        
    def disable(self):
        self.setEnabled(False)
        
        
        
    def setGlobalEnabled(self, state):
        for rowControl in self.rowControls:
            rowControl.setGlobalEnabled(state)

    def globalEnable(self):
        self.setGlobalEnabled(True)
        
    def globalDisable(self):
        self.setGlobalEnabled(False)
        


def _createButton (label, alignment):
    if alignment is not None:
        button = pyxbmct.Button(label, alignment=alignment)
    else:
        button = pyxbmct.Button(label)
        
    return button