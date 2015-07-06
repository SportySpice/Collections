import pyxbmct.addonwindow as pyxbmct
from Row import Row
from src.li.visual import TextSettings as ts
import src.tools.addonSettings as addon


SETTING_COLUMN = 2
SETTING_COLUMN_PAD = 2

#MAX_PAGE_ROWS = 12
BUTTON_ROW = 13


TABS_COLOR = None





class SettingsWindow(object):
    def __init__(self, title, width=800, height=500, saveCallback=None, hideTabs=False, showButtons=True):
        self.title = title
        self.width = width
        self.height = height        
        self.saveCallback = saveCallback
        self.hideTabs = hideTabs
        
        self.window = pyxbmct.AddonDialogWindow(title)
        self.window.setGeometry(width, height, 14, 10)
        
        if showButtons:
            self.createButtons()
        else:
            self.buttonRow = None
        
        
        self.tabs = []
        self.onSaveCallbacks = []
        
        self.currentPage = None
        
        
        
    def createButtons(self):
        buttonRow = Row()

        def defaultsActions():
            for onDefaultCallback in self.currentPage.tab.onDefaultCallbacks:
                onDefaultCallback()
        
        def okAction():
            for onSaveCallback in self.onSaveCallbacks:
                onSaveCallback()
                
            if self.saveCallback:
                self.saveCallback()
                
            self.window.close()


        def cancelAction():
            self.window.close()
            
            
        buttonRow.addButton(    addon.string(600),  2,      okAction,        columnspan=2, bold=True)
        buttonRow.addButton(    addon.string(601),  4,      cancelAction,    columnspan=2, bold=True)
        buttonRow.addButton(    addon.string(602),  6,      defaultsActions, columnspan=2, bold=True)
        
        
                
        self._placeRow(buttonRow, BUTTON_ROW, forceLocation=True)                
        self.buttonRow = buttonRow
        


    def addCustomButton(self, label, column, onClick):
        if self.buttonRow is None:
            self.buttonRow = Row()
            
        button = self.buttonRow.addButton(label,             column, onClick,         columnspan=2, bold=True)
        return button
            
    
    def placeCustomButtons(self):    
        self._placeRow(self.buttonRow, BUTTON_ROW, forceLocation=True)
        




    def _placeRow(self, row, rowNum, onDefaultCallbacks=None, forceLocation=False):
        for rowControl in row.rowControls:            
            column = rowControl.column
            columnspan = rowControl.columnspan 
            if self.hideTabs and column == SETTING_COLUMN and not forceLocation:
                column -= 2
                columnspan += 2
            
            #column +=1
                
            self.window.placeControl(rowControl.control, rowNum, column, columnspan=columnspan, pad_x=rowControl.padX, rowspan=rowControl.rowspan)
                                            
            if rowControl.action:
                self.window.connect(rowControl.control, rowControl.action)

            if rowControl.onDefault:
                onDefaultCallbacks.append(rowControl.onDefault)
                
            if rowControl.onSave:
                self.onSaveCallbacks.append(rowControl.onSave)
                
            if rowControl.init:
                rowControl.init()
        
        
        
            
            
        
        
        
        

        
    def addTabs(self, tabs, bold=False, space=10, padX=-10, textXOffset=0):        
        listC = pyxbmct.List(_space=space, _itemTextXOffset=textXOffset)
        
        if not self.hideTabs:
            self.window.placeControl(listC, 0, 0, 10, 2, pad_x=padX)
        
        
        index = 0
        for tab in tabs:
            title = tab.title
            title = ts.color(TABS_COLOR, title)
            
            if bold:
                title = ts.bold(title)
            
            listC.addItem(title)
        
            tab.num = index            
            self.tabs.append(tab)
            
            self.window.setGeometry(self.width, self.height, tab.numRows, tab.numColumns)                               
            self.placeTab(tab)            
            
            index += 1
            
            
        self.tabsListC = listC
        
        
        self.showTab(0)
        self.window.connect(listC, self.tabAction)
        
        
        
    def tabAction(self):
        tabIndex = self.tabsListC.getSelectedPosition()
        self.showTab(tabIndex)
        
      
      
    def showPage(self, page):
        if self.currentPage == page:
            return
        
        if self.currentPage is not None:
            self.currentPage.hide()
            
            currentTab = self.currentPage.tab
            if currentTab.useGlobalButton:
                currentTab.ugbRow.hide()
                
            
        
                    
        page.unHide() 
        self.currentPage = page
        
        
        tab = page.tab
        if tab.useGlobalButton:
            tab.ugbRow.unHide()
            
        
        
        
    def showTab(self, tabIndex, pageNum=0):
        tab = self.tabs[tabIndex]
        page = tab.pages[pageNum]
        
        self.showPage(page)
                

    
    
    
    
    
        
        
        
    def placeTab(self, tab):
        pages = []
        onDefaultCallbacks = []       
         
        currentPage = TabPage(0, tab, self)                
        pages.append(currentPage)
        
        
        
        for row in tab.rows:            
            #if currentPage.rowsFilled == MAX_PAGE_ROWS:
            if currentPage.rowsFilled == tab.numRows - 2:
                lastPage = currentPage
                currentPage = TabPage(lastPage.num + 1, tab, self, prevPage=lastPage)                     
                lastPage.addNextPage(currentPage)
    
                pages.append(currentPage)
            
            
            self._placeRow(row, currentPage.rowsFilled, onDefaultCallbacks)
            currentPage.addRow(row)            
                                        

        
        for page in pages:
            page.placeNavRowIfExists()
            page.hide()
        
        
        tab.onDefaultCallbacks = onDefaultCallbacks
        tab.pages = pages
        
        
        
        if tab.useGlobalButton:
            ugbRow = Row()
                        
            ugb = tab.useGlobalButton                   
            label = ts.italic( addon.string(605) )
            ugbRow.addRadioButton(7, ugb.current, ugb.default, saveCallback=ugb.saveCallback, label=label, columnspan=2, changeCallback=lambda state: tab.setGlobalEnabled(not state))
            
            self.window.setGeometry(self.width, self.height, 14, 10)
            self._placeRow(ugbRow, 12, onDefaultCallbacks)
            
            ugbRow.hide()            
            tab.ugbRow = ugbRow
            
    
            if ugb.current is True:
                tab.globalDisable()
                
            
    

    
    
    
                
    
    
    
    
                
               
            
    def show(self):
        self.window.doModal()
        
    def close(self):
        self.window.close()
        
        
    
    def delete(self):
        del self.window
        
        
        
class TabPage():
    def __init__(self, pageNum, tab, window, prevPage=None):        
        self.num = pageNum
        self.tab = tab
        self.window = window
        
        self.rows = []
        self.rowsFilled = 0        
        
        if prevPage:                                    
            self.navRow = Row()
            self.navRow.addButton(addon.string(603), 8, lambda: self.window.showPage(prevPage), columnspan=1, bold=False)
        else:
            self.navRow = None
        
        
        
    

        
        
    def addRow(self, row):
        self.rows.append(row)
        self.rowsFilled += 1
        
        
  
    def addNextPage(self, nextPage):
        if self.navRow is None:                
            self.navRow = Row()
            
        self.navRow.addButton(addon.string(604), 9, lambda: self.window.showPage(nextPage), columnspan=1, bold=False)
        
    
    def placeNavRowIfExists(self):
        if self.navRow:
            self.window._placeRow(self.navRow, BUTTON_ROW)
    
    
    
    
    
    def setVisible(self, state):
        for row in self.rows:
            row.setVisible(state) 
        
        if self.navRow:
            self.navRow.setVisible(state) 
            
    def hide(self):
        self.setVisible(False)
        
                        
    def unHide(self):
        self.setVisible(True)                                              