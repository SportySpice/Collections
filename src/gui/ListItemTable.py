from Tab import SETTING_COLUMN, SETTING_COLUMN_PAD
from Row import Row
from EnumButton import EnumMode
import colors
import pyxbmct.addonwindow as pyxbmct
from src.li.visual.CountTextSettings import Location, CountTextSettings, CountType as ct
from src.li.visual import FullTextSettings
from src.li.visual import TextSettings
from src.tools.addonSettings import string as st




# COUNT_OPTIONS           =   (ct.VIEWS,      ct.SUBSCRIBERS,     ct.VIDEOS,      ct.NEW_VIDEOS)
# COUNT_LABELS            =   (st(662),       st(663),            st(664),        st(665))
ctToLabel   =   {ct.VIEWS:st(665),  ct.SUBSCRIBERS:st(666),   ct.VIDEOS:st(667),     ct.NEW_VIDEOS:st(668)}



LOCATION_OPTIONS        =   (Location.LEFT,     Location.MIDDLE,        Location.RIGHT)
LOCATION_LABELS         =   (st(670),           st(671),               st(672))







COLOR_COLUMN = 5
BOLD_COLUMN = 6
ITALIC_COLUMN = 7

LOCATION_COLUMN = 8
LOCATION_COLUMN_PAD = 15
LOCATION_COLUMN_SPAN = 2




class ListItemTable(object):
    def __init__(self):
        self.rows = []
        #self.exampleRows = []
                        
        headingRow = Row()
        
        headingRow.addLabel(    st(650),    COLOR_COLUMN,   columnspan=2, bold=True)
        headingRow.addLabel(    st(651),    BOLD_COLUMN,    columnspan=2, bold=True, padX=23)
        headingRow.addLabel(    st(652),    ITALIC_COLUMN,  columnspan=3, bold=True, padX=23)
        #headingRow.addLabel(   st(653),    LOCATION_COLUMN,columnspan=2, bold=True, padX=LOCATION_COLUMN_PAD,     alignment=pyxbmct.ALIGN_LEFT)
        #headingRow.addLabel(   st(653),    LOCATION_COLUMN,columnspan=2, bold=True, padX=LOCATION_COLUMN_PAD+23,  alignment=pyxbmct.ALIGN_LEFT)        
        self.rows.append(headingRow)        
        
        
        self.exampleRow = Row()
        #self.examplesTB = self.exampleRow.addTextBox(SETTING_COLUMN, columnspan=7, padX=SETTING_COLUMN_PAD, rowspan=5)
        self.exampleList = None        
        self.examples = []
        
        self._assignedValue = False
        
        
        
    
    def updateExamples(self):
        examplesToShow = []        
        for example in self.examples:
            if example.visible:
                examplesToShow.append(example.text)
        
        if self.exampleList:
            self.exampleList.control.reset()
            for example in examplesToShow:
                self.exampleList.control.addItem(example) 
        
        else:
            self.exampleList = self.exampleRow.addList(examplesToShow, SETTING_COLUMN, space=0, columnspan=7, rowspan=7)

        
        
        #examplesText = '\n'.join(examplesToShow)
        #self.examplesTB.setText(examplesText)
    
    
    def addCustomItem(self, label, currentTS, defaultTS, saveCallback, showOptions=False, radioPadX=0):
        
        assignedTS = TextSettings.fromOther(currentTS)
        
        
            
        
        #exampleRow = Row()
        #example = exampleRow.addLabel(exampleText(), SETTING_COLUMN, columnspan=7, padX=SETTING_COLUMN_PAD, alignment=pyxbmct.ALIGN_LEFT)
                    
        example = Example(assignedTS.apply(label), self, assignedTS.show)
        self.examples.append(example)
        
        def exampleUpdate():            
            exampleText = assignedTS.apply(label)
            example.update(exampleText, assignedTS.show)
            
            
            #example.setLabel(exampleText())
            
        self.addItemRow(label, currentTS, defaultTS, assignedTS, exampleUpdate, showOptions, saveCallback=saveCallback, radioPadX=radioPadX)
        #self.exampleRows.append(exampleRow)
        
        
        
        
        
        
        
        
    def addFullItem(self, currentFTS, defaultFTS, saveCallback, titleExample, sourceExample=None, countExample=None, countlessTitleExample=None, countlessSourceExample=None):
        assignedFTS = FullTextSettings.fromOther(currentFTS)
        _saved = [False]
        
        
        def onSave(assignedTS):           #this function prevents saveCallback to be called more than once by the other TSes
            if not _saved[0]:   
                saveCallback(assignedFTS)
                _saved[0] = True
        
        def exampleText():
            return assignedFTS.fullText(titleExample, sourceExample, countExample)
         
        def countlessExampleText():
            return assignedFTS.fullText(countlessTitleExample, countlessSourceExample)
#             countTS = assignedFTS.countTS        
#             assignedFTS.countTS = None        
#             text = assignedFTS.fullText(countlessTitleExample, countlessSourceExample)
#              
#             assignedFTS.countTS = countTS
#             return text

        
        
        example = Example(exampleText(), self)
        countlessExample = Example(countlessExampleText(), self) 
        self.examples.append(example)
        self.examples.append(countlessExample)
        
        def exampleUpdate():                        
            example.update(exampleText())
            countlessExample.update(countlessExampleText())
            
            
        
        
        radioPadX = 0
        #radioPadX = -14
        label = ctToLabel[currentFTS.countTS.countType]
        self.addItemRow(label, currentFTS.countTS, defaultFTS.countTS, assignedFTS.countTS, exampleUpdate, showOptions=True, saveCallback=onSave, radioPadX=radioPadX) 
                     
        label = st(660)       
        radioPadX = 0
        #radioPadX = -14
        self.addItemRow(label, currentFTS.sourceTS, defaultFTS.sourceTS, assignedFTS.sourceTS, exampleUpdate, showOptions=True, saveCallback=onSave, radioPadX=radioPadX)
                                        
        label = st(661)
        self.addItemRow(label, currentFTS.titleTS, defaultFTS.titleTS, assignedFTS.titleTS, exampleUpdate, saveCallback=onSave)    
            


        #exampleRow          = Row()
        #countlessExampleRow = Row()                        
        #example          =  exampleRow          .addLabel(exampleText(),            SETTING_COLUMN, columnspan=7, padX=SETTING_COLUMN_PAD, alignment=pyxbmct.ALIGN_LEFT)        
        #countlessExample =  countlessExampleRow .addLabel(countlessExampleText(),   SETTING_COLUMN, columnspan=7, padX=SETTING_COLUMN_PAD, alignment=pyxbmct.ALIGN_LEFT)
        
        #def exampleUpdate():
            #example.setLabel(exampleText())
            #countlessExample.setLabel(countlessExampleText())
            #pass      
            
        #self.exampleRows.append(exampleRow)
        #self.exampleRows.append(countlessExampleRow)
        
        
        
        
        
        
        
    def addItemRow(self, label, currentTS, defaultTS, assignedTS, exampleUpdate, showOptions=False, saveCallback=None, radioPadX=0):
        _assignedValue = [False]
        
        
        def assignedValue():
            exampleUpdate()
            _assignedValue[0] = True
        
        
        def colorCallback(color):
            assignedTS.color = color
            assignedValue()
        
        def boldCallback(state):
            assignedTS.bold = state
            assignedValue()
            
        def italicCallback(state):
            assignedTS.italic = state
            assignedValue()
            
        def onSave(value):
            if _assignedValue[0] and saveCallback:                
                saveCallback(assignedTS)
                _assignedValue[0] = None     #so saveCallback doesn't get called again and again from the other controls
                
        
        
        
        row = Row()
        
        if showOptions:
            def setButtonsState(state):
                colorButton.setEnabled(state)
                boldButton.setEnabled(state)
                italicButton.setEnabled(state)
                if locationButton:
                    locationButton.setEnabled(state)
            
            
            def showCallback(state):
                assignedTS.show = state
                setButtonsState(state)
                assignedValue()                    
                    
            
                
            radioMove = 30 + radioPadX
            padX = SETTING_COLUMN_PAD - radioMove
            textOffsetX = radioMove
            
            row.addRadioButton(SETTING_COLUMN, assignedTS.show, defaultTS.show, label=label, changeCallback=showCallback, saveCallback=onSave, columnspan=1, padX=padX, textOffsetX=textOffsetX, alignment=pyxbmct.ALIGN_LEFT)
            #row.addRadioButton(LOCATION_COLUMN, assignedTS.show, defaultTS.show, changeCallback=showCallback, saveCallback=onSave, columnspan=LOCATION_COLUMN_SPAN, padX=LOCATION_COLUMN_PAD)
            
            buttonsEnabled = assignedTS.show
            
        else:
            row.addLabel(label, SETTING_COLUMN, columnspan=3, padX=SETTING_COLUMN_PAD, alignment=pyxbmct.ALIGN_LEFT)
            buttonsEnabled = True
                
        colorButton = row.addEnumButton(st(650), colors.loweredColors, currentTS.color, defaultTS.color, COLOR_COLUMN, customLabels=colors.coloredColors, alignment=pyxbmct.ALIGN_LEFT, columnspan=1, changeCallback=colorCallback, saveCallback=onSave, returnValue=True, mode=EnumMode.SELECT, enabled=buttonsEnabled)
        boldButton = row.addRadioButton(BOLD_COLUMN, currentTS.bold, defaultTS.bold, changeCallback=boldCallback, saveCallback=onSave, enabled=buttonsEnabled)
        italicButton = row.addRadioButton(ITALIC_COLUMN, currentTS.italic, defaultTS.italic, changeCallback=italicCallback, saveCallback=onSave, enabled=buttonsEnabled)        

   
            
        if type(assignedTS) is CountTextSettings:             
            def locationCallback(location):            
                assignedTS.location = location
                assignedValue()
                 
             
            locationButton = row.addEnumButton(st(653), LOCATION_OPTIONS, currentTS.location, defaultTS.location, LOCATION_COLUMN, changeCallback=locationCallback, saveCallback=onSave, customLabels=LOCATION_LABELS, returnValue=True, alignment=pyxbmct.ALIGN_LEFT, columnspan=LOCATION_COLUMN_SPAN, padX=LOCATION_COLUMN_PAD, enabled=buttonsEnabled)
            
        else:
            locationButton = None
                 


        if showOptions:
            setButtonsState(assignedTS.show)
        
        self.rows.append(row)
        

    

        
    
    
    
    def addExamples(self):
        #self.rows.extend(self.exampleRows)
        self.updateExamples()
        self.rows.append(self.exampleRow)
        
        
    def addEmptyRow(self):
        row = Row()
        self.rows.append(row)
    
        


class Example(object):
    def __init__(self, text, liTable, visible=True):
        self.text = text
        self.visible = visible
        self.liTable = liTable
        
    
    def update(self, text, visible=True):
        self.text=text        
        self.visible = visible
        self.liTable.updateExamples()