import TextSettings
from src.tools.enum import enum

Location = enum(LEFT_ALIGNED=1, LEFT=2, MIDDLE=3, RIGHT=4)

class FullTextSettings(object):
    def __init__(self, titleTS, sourceTS=None, countTS=None, count2TS=None, countLocation=None):                
        self.titleTS = titleTS
        self.sourceTS = sourceTS
        self.countTS = countTS
        self.count2TS = count2TS
        self.countLocation = countLocation
        
        
        
    
            
    def titleText(self, text):
        return self.titleTS.apply(text)
    
    
    def sourceText(self, text):
        if self.sourceTS is None:
            raise ValueError('This title has no source text')
                
        return self.sourceTS.apply(text + ':')
    
    
    def countText(self, number, ts):
        if ts is None:
            raise ValueError('This title has no count text')
                 
        if number is None:
            return '', '', 0
        
        text = str(number)
        textLen = len(text)
        coloredText = ts.apply(text)
        
        return coloredText, text, textLen

    
    
    
    def fullText(self, titleText, sourceText=None, countNumber=None, maxChars=None, textIfNone=None, countNumber2=None, maxChars2=None, textIfNone2=None, hasCount2=True):                
        if self.sourceTS.show:            
            leftText = self.sourceText(sourceText) + ' '
            rightText = self.titleText(titleText)
            
        else:
            leftText = ''
            rightText = self.titleText(titleText)
                
        if not self.countTS.show:
            return leftText + rightText
        

        
        
        
        count1Colored, count1Origin, count1Len = self.countText(countNumber,  self.countTS)
        
        if self.count2TS:
            count2Colored, count2Origin, count2Len = self.countText(countNumber2, self.count2TS)
        else :           
            count2Colored, count2Origin, count2Len = None, None, None
            hasCount2 = False
        
        if self.countLocation == Location.LEFT_ALIGNED:
            if countNumber is None:
                if textIfNone:
                    count1Colored = self.countTS.apply(textIfNone)
                else:
                    count1Colored = ''
                
            else:
                if maxChars:
                    spacesToAdd  = maxChars - count1Len + 1
                    if ('m' in count1Origin) or ('w' in count1Origin):
                        spacesToAdd -= 1
                    if spacesToAdd >0:
                        count1Colored = count1Colored + '  '*spacesToAdd
                    
            
            countText = count1Colored
            
            if hasCount2:            
                if countNumber2 is None:
                    if textIfNone2:
                        count2Colored = self.count2TS.apply(textIfNone2)
                    else:
                        count2Colored = ''
                                    
                else:                    
                    if maxChars2:
                        spacesToAdd = maxChars2 - count2Len + 1
                        if ('m' in count2Origin) or ('w' in count2Origin):
                            spacesToAdd -= 1
                        count2Colored = count2Colored + '  '*spacesToAdd                                            
                        #count2Colored =  '  '*spacesToAdd + count2Colored
                            
                countText += ' ' + count2Colored 
            
            countText += ' '
        
        
        
        
        else:
            if count1Colored or count2Colored:
                countText = '(' + count1Colored
                if count2Colored:
                    countText +=  '  ' + count2Colored + ')'
                else:
                    countText += ')'
                
            else:
                countText = ''
            


        if (self.countLocation == Location.LEFT_ALIGNED) or (self.countLocation == Location.LEFT):
            return countText + ' '+  leftText  + rightText
        
        if self.countLocation == Location.MIDDLE:
            return leftText + countText + ' '  + rightText
        
        #right
        return leftText +  rightText + ' ' + countText 
    
    
    
def _fromOtherTS(ts):
    if ts is None:
        return None
        
    return  TextSettings.fromOther(ts)
    
def fromOther(fts):
    titleTS  = _fromOtherTS(fts.titleTS)    
    sourceTS = _fromOtherTS(fts.sourceTS)    
    countTS  = _fromOtherTS(fts.countTS)
    count2TS = _fromOtherTS(fts.count2TS)
    countLocation = fts.countLocation
    
    
        
    return FullTextSettings(titleTS, sourceTS, countTS, count2TS, countLocation)