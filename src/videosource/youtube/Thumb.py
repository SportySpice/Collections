from src.tools.enum import enum

ThumbRes = enum (MEDIUM=0, HIGH_OR_LOWER=1, HIGH_OR_BETTER=2, HIGHEST=3)

class Thumb(object):

    def __init__(self, thumbnailDetails):
        self.default = None
        self.standard = None
        self.medium = None
        self.high = None
        self.max = None

        nonRecieved = True
        
        if 'default' in thumbnailDetails:
            self.default = thumbnailDetails['default']['url']
            nonRecieved = False
        
        if 'standard' in thumbnailDetails:
            self.standard = thumbnailDetails['standard']['url']
            nonRecieved = False
                        
        if 'medium' in thumbnailDetails:
            self.medium = thumbnailDetails['medium']['url']
            nonRecieved = False
            
        if 'high' in thumbnailDetails:
            self.high = thumbnailDetails['high']['url']
            nonRecieved = False
            
        if 'maxres' in thumbnailDetails:
            self.max = thumbnailDetails['maxres']['url']
            nonRecieved = False
            
        if nonRecieved:
            raise ValueError('Expected to receive at least one thumbnail but received none')
            
    
    
    
    def _selectQuality(self, qualityOrder):
        for quality in qualityOrder:
            if quality is not None:
                return quality
        
            
            
    ##all methods below are probably not 100% accurate as I'm
    ##not sure exactly what the quality of "standard" and "default" is
             
    



    def mediumRes(self):
        qualityOrder = (self.medium, self.high, self.standard, self.default, self.max)
        return self._selectQuality(qualityOrder)
    
    def highOrLower(self):
        qualityOrder = (self.high, self.standard, self.default, self.medium, self.max, )
        return self._selectQuality(qualityOrder)


    def highOrBetter(self):
        qualityOrder = (self.high, self.standard, self.default, self.max, self.medium)
        return self._selectQuality(qualityOrder)
    
    
    def highest(self):
        qualityOrder = (self.max, self.high, self.standard, self.default, self.medium)
        return self._selectQuality(qualityOrder)
    
        
    
    def get(self, thumbRes):
        types = {ThumbRes.MEDIUM:self.mediumRes, ThumbRes.HIGH_OR_LOWER:self.highOrLower,
                 ThumbRes.HIGH_OR_BETTER:self.highOrBetter, ThumbRes.HIGHEST:self.highest}
        
        return types[thumbRes]()

    
