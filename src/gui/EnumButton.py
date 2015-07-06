from src.tools.enum import enum
import pyxbmct.addonwindow as pyxbmct
from src.tools.dialog import dialog


EnumMode = enum(SELECT=0, ROTATE=1)


class EnumButton(object):
    def __init__(self, label, values, current, default, changeCallback=None, saveCallback=None, customLabels=None, mode=EnumMode.SELECT, returnValue=False, alignment=pyxbmct.ALIGN_CENTER):
        
        self.label = label
        self.values = values
        self.customLabels = customLabels
        self.mode = mode
        self.returnValue = returnValue
        self.changeCallback = changeCallback
        self.saveCallback = saveCallback

        
        
        self.currentValue = current
        self.defaultValue = default        
        self.currentIndex = None        
        self.defaultIndex = None
        
                
        self.assignedValue = False
        
        if saveCallback is None:
            self.onSave = None
        
        
        
        if customLabels:
            self._findCurrentIndex()
            label = str(customLabels[self.currentIndex])
            
        else:
            label = str(current)
        
        
        if alignment is not None:
            self.button = pyxbmct.Button(label, alignment=alignment)
        else:
            self.button = pyxbmct.Button(label)
            
            
            
    
    
    def update(self, value):
        if self.currentValue != value:
            self.currentValue = value
            
            if self.customLabels:
                self._findCurrentIndex()
                label = str(self.customLabels[self.currentIndex])
            
            else:
                self.currentIndex = None
                label = str(value)
                
            self.button.setLabel(label)
            self.assignedValue = True
            
        
            
            
            
    def onClick(self):
        if self.mode == EnumMode.SELECT:
            if self.customLabels:
                values = self.customLabels
            else:
                values = self.values
            
            selectedIndex = dialog.select(self.label, list((str(value) for value in values)))
            if selectedIndex == -1:
                return
            
            index = selectedIndex
            
            
        else:        
            if self.currentIndex is None:
                self._findCurrentIndex()
                
            if self.currentIndex  == len(self.values) - 1:
                index = 0
            else:
                index = self.currentIndex + 1
                
        self.assign(index)   
        
        
        
    def onDefault(self):
        if self.defaultIndex is None:            
            self._findDefaultIndex()
            
        self.assign(self.defaultIndex)          
        
        
    def onSave(self):
        if self.assignedValue:
            if self.returnValue:
                self.saveCallback(self.currentValue)
            else:            
                self.saveCallback(self.currentIndex)   
            
           
           
           
            
    def assign(self, index):
        value = self.values[index]
        self.currentIndex = index                
        self.currentValue = value
                    
        if self.customLabels:
            label = str(self.customLabels[index])
        else:
            label = str(value)
            
        self.button.setLabel(label)
        self.assignedValue = True
        
        
        if self.changeCallback:
            if self.returnValue:
                self.changeCallback(value)
            else:        
                self.changeCallback(index)
        
        
        
    

            
        
            
        
        
        
            
            
            
            
    def _findDefaultIndex(self):
        for i in range(0, len(self.values)):
            value = self.values[i]
            if value == self.defaultValue:
                self.defaultIndex = i
                    
        if self.defaultIndex is None:
            raise ValueError ('Default value not found in value list')
        
        
        
    def _findCurrentIndex(self):
        for i in range(0, len(self.values)):
            value = self.values[i]
            if value == self.currentValue:
                self.currentIndex = i
                    
        if self.currentIndex is None:
            raise ValueError ('Current value not found in value list')