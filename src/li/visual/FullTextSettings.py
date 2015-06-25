from src.li.visual.CountTextSettings import Location
import TextSettings
from src.li.visual import CountTextSettings

class FullTextSettings(object):
    def __init__(self, titleTS, sourceTS=None, countTS=None):                
        self.titleTS = titleTS
        self.sourceTS = sourceTS
        self.countTS = countTS
        
        
        
    
            
    def titleText(self, text):
        return self.titleTS.apply(text)
    
    
    def sourceText(self, text):
        if self.sourceTS is None:
            raise ValueError('This title has no source text')
                
        return self.sourceTS.apply(text + ':')
    
    
    def countText(self, number):
        if self.countTS is None:
            raise ValueError('This title has no count text')
                
        return self.countTS.apply(number)

    
    
    
    def fullText(self, titleText, sourceText=None, countNumber=None):                
        if self.sourceTS.show:            
            leftText = self.sourceText(sourceText) + ' '
            rightText = self.titleText(titleText)
            
        else:
            leftText = ''
            rightText = self.titleText(titleText)
        
        
        if (countNumber is None) or (not self.countTS.show):
            return leftText + rightText
        
        
        countText = self.countText(countNumber)
        
        
        
        if self.countTS.location == Location.LEFT:
            return countText + ' '+  leftText  + rightText
        
        if self.countTS.location == Location.MIDDLE:
            return leftText + countText + ' '  + rightText
        
        #right
        return leftText +  rightText + ' ' + countText 
    
    
    
def fromOther(fts):
    titleTS = TextSettings.fromOther(fts.titleTS)
    
    sourceTS = fts.sourceTS
    if sourceTS:
        sourceTS = TextSettings.fromOther(sourceTS)
        
    countTS = fts.countTS
    if countTS:
        countTS = CountTextSettings.fromOther(countTS)
        
    return FullTextSettings(titleTS, sourceTS, countTS)