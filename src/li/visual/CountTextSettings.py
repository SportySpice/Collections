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
        
        #countText = '{:,}'.format(number)    # only works on python 2.7+
        countText = intWithCommas(number)
        countText = '(%s)' % super(CountTextSettings, self).apply(countText)
        
        return countText


def intWithCommas(number):
    if type(number) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if number < 0:
        return '-' + intWithCommas(-number)
    result = ''
    while number >= 1000:
        number, r = divmod(number, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (number, result)


# def intWithCommas2(number):
#     s = '%d' % number
#     groups = []
#     while s and s[-1].isdigit():
#         groups.append(s[-3:])
#         s = s[:-3]
#     return s + ','.join(reversed(groups))




    
    
    
def fromOther(countTS):
    c = countTS
    return CountTextSettings(c.color, c.bold, c.italic, c.location, c.countType, c.show)






