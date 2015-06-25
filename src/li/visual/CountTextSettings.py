from TextSettings import TextSettings
from src.tools.enum import enum

#Location = enum(OFF=False, LEFT=1, MIDDLE=2, RIGHT=3)
Location = enum(LEFT=1, MIDDLE=2, RIGHT=3)
CountType = enum (VIEWS=1, SUBSCRIBERS=2, VIDEOS=3, NEW_VIDEOS=4)


class CountTextSettings(TextSettings):
    def __init__(self, color, bold, italic, location, countType, show=True):        
        super(CountTextSettings, self).__init__(color, bold, italic, show)
        
        self.location = location
        self.countType = countType
        
        
        
    #overrides original method        
    def apply(self, number):
        if not self.show:
            return ''
        
        countText = '{:,}'.format(number)
        countText = '(%s)' % super(CountTextSettings, self).apply(countText)
        
        return countText
    
    
    
def fromOther(countTS):
    c = countTS
    return CountTextSettings(c.color, c.bold, c.italic, c.location, c.countType, c.show)