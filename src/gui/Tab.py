from SettingsWindow import SETTING_COLUMN, SETTING_COLUMN_PAD
from Row import Row, EnumMode
from src.li.visual import TextSettings as ts
import pyxbmct.addonwindow as pyxbmct
import xbmcgui


LABELS_BOLD = False
LABEL_COLOR = None


VALUE_COLUMN = 7
VALUE_COLUMN_SPAN = 3

class Tab(object):
    def __init__(self, title, rows=15, columns=10):
        self.title = title
        self.numRows = rows
        self.numColumns = columns
        
        self.rows = []
        self.useGlobalButton = None
        

    
    
    def addRow(self, row):
        self.rows.append(row)
        
    def addSettingRow(self, label):
        label = ts.color(LABEL_COLOR, label)
        
        row = Row()
        row.addLabel(label, SETTING_COLUMN, 5, SETTING_COLUMN_PAD, pyxbmct.ALIGN_LEFT, bold=LABELS_BOLD)
        
        self.addRow(row)
        return row
        
        
        
    def addEnum(self, label, values, current, default, onSave, customLabels=None, mode=EnumMode.SELECT, returnValue=True, changeCallback=None):
        row = self.addSettingRow(label)
        button = row.addEnumButton(label, values, current, default, VALUE_COLUMN, onSave, customLabels=customLabels, mode=mode, returnValue=returnValue, 
                           changeCallback=changeCallback, alignment=pyxbmct.ALIGN_LEFT, columnspan=VALUE_COLUMN_SPAN)        
        
        return button
        
    def addBool(self, label, current, default, onSave):
        row = self.addSettingRow(label)
        row.addRadioButton(VALUE_COLUMN, current, default, onSave, columnspan=VALUE_COLUMN_SPAN)

        
    def addInputEdit(self, label, current, default, onSave):
        row = self.addSettingRow(label)
        row.addInputEdit(label, VALUE_COLUMN, current, default, onSave, columnspan=VALUE_COLUMN_SPAN)
        
    def addInputButton(self, label, current, default, onSave, inputType=xbmcgui.INPUT_ALPHANUM):
        row = self.addSettingRow(label)
        row.addInputButton(label, VALUE_COLUMN, current, default, onSave, inputType=inputType,
                            alignment=pyxbmct.ALIGN_LEFT, columnspan=VALUE_COLUMN_SPAN)
        
    
    def addButton(self, label, onClick, bold=False, columnSpan=3, centered=False):
        row = Row()                
        
        if centered:
            column = self.numColumns / 2
        else:
            column = SETTING_COLUMN
            
        button = row.addButton(label, column, onClick, columnspan=columnSpan,  padX=-5, alignment=pyxbmct.ALIGN_LEFT, bold=bold)        
        self.addRow(row)
        
        return button
    
    
        
    def addEmptyRow(self):
        row = Row()
        self.addRow(row)
        
        
    def addListItemTable(self, listItemTable):
        for row in listItemTable.rows:
            self.addRow(row)
            
            
            
    def addUseGlobalButton(self, current, default, saveCallback):
        self.useGlobalButton = UseGlobalButton(current, default, saveCallback)
        
        
    def setEnabled(self, state):
        for row in self.rows:
            row.setEnabled(state)
            
    def enable(self):
        self.setEnabled(True)
            
    def disable(self):
        self.setEnabled(False)
        
        
    def setGlobalEnabled(self, state):
        for row in self.rows:
            row.setGlobalEnabled(state)

    def globalEnable(self):
        self.setGlobalEnabled(True)
        
    def globalDisable(self):
        self.setGlobalEnabled(False)    
        
        
        
        
        
        
class UseGlobalButton(object):
    def __init__(self, current, default, saveCallback):
        self.current = current
        self.default = default
        self.saveCallback = saveCallback