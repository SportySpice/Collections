class OrderedSettings:
    def __init__(self):
        self._list = []
        self._dic = {}
        
    def add(self, key, value, customValue=None, customValueDic=None, nonePossible=False):
        if customValue:
            value = customValue
                
        if customValueDic:
            if (not nonePossible) or (value is not None):
                value = customValueDic[value]
        
        self._dic[key] = value
        
        setting = Setting(key, value)
        self._list.append(setting)
        
        
        
    def addIfNotNone(self, key, value, customValue=None, customValueDic=None):
        if value is not None:                
            self.add(key, value, customValue, customValueDic)
            
            
    def addIfDifferent(self, key, value, comparisonValue, customValue=None, customValueDic=None, nonePossible=False):
        if value != comparisonValue:
            self.add(key, value, customValue, customValueDic, nonePossible)
        
        
    def insert(self, index, key, value):
        self._dic[key] = value
        
        setting = Setting(key, value)
        self._list.insert(index, setting)
        
        
    
    def list(self):
        return self._list
    
    
    def hasValues(self):
        if self._list:
            return True
        
        return False
    
    
    
class Setting:
    def __init__(self, key, value):
        self.key = key
        self.value = value