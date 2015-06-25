from src.file import File

loadedDics = {}

class DataDictionary(object):
    def __init__(self, dicFile):
        self.dicFile = dicFile
        
        if dicFile.exists():
            self.dic = dicFile.loadObject()
        else:        
            self.dic = {}
            
        global loadedDics
        loadedDics[dicFile.fullpath] = self
        
        
      
    def has(self, key):
        if key in self.dic:
            return True
        
        return False  
    
    
    
    def get(self, key):
        return self.dic[key]
    
    
    
    def set(self, key, value):
        self.dic[key] = value
        self.dicFile.dumpObject(self.dic)
    

    def setIfNonExistent(self, key, value):
        if key in self.dic:
            if self.dic[key] != value:
                raise ValueError('Received a different value for the same key. This should never happen.')
            
            return
            
                        
        self.set(key, value)
    
        
    
    
        
        
        
def _loadFromMemory(path):
    global loadedDics    
    if path in loadedDics:
        return loadedDics[path]
    
    return None
        
        

def load(fileName, fileDir):
    fullpath = fileDir + '/' + fileName
    
    dataDic = _loadFromMemory(fullpath)
    if dataDic:
        return dataDic
    
    dicFile = File.fromFullpath(fullpath)
    return DataDictionary(dicFile)