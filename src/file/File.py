import xbmc
import xbmcvfs
import Folder
import urllib
import urlparse


NAME_QUERY = 'fileName'
FOLDER_NAME_QUERY = 'folderName'
FOLDER_PATH_QUERY = 'folderPath'






class File(object):
    def __init__(self, name, folder):
        self.name = name
        self.folder = folder
        self.path = folder.fullpath
        self.fullpath = folder.fullpath + '/' + name
        
        if '.' in name:
            self.soleName, self.extension = name.split('.', 1)
        else:
            self.soleName = name
            self.extension = None
         
        
        self._pathTranslated = None
        self._fullpathTranslated = None
    
    
    def exists(self):
        return xbmcvfs.exists(self.fullpath)
    
    def delete(self):
        xbmcvfs.delete(self.fullpath)
        
        
    def deleteIfExists(self):
        if self.exists():
            self.delete()
        
        
    def pathTranslated(self):
        return self.folder.fullpathTranslated()
        
        
        
    def fullpathTranslated(self):
        if self._fullpathTranslated is None:            
            self._fullpathTranslated = xbmc.translatePath(self.fullpath)
            
        return self._fullpathTranslated
    
    
    
    def fileHandler(self, write=False):
        if write:
            permission = 'w'
        else:
            permission = 'r'
        
        fullpath = self.fullpathTranslated()
        return xbmcvfs.File(fullpath, permission)
    
    def contents(self):
        fh = self.fileHandler();
        
        contents = fh.read()
        fh.close()
        
        return contents
        
    
    def lines(self):
        contents = self.contents()
        return contents.split('\n')
    
    
    def write(self, contentsStr):
        fh = self.fileHandler(write=True)
        fh.write(contentsStr)
        fh.close()
        
    
    
    def encodedQuery(self):
        query = urllib.urlencode({NAME_QUERY: self.name,
                                  FOLDER_NAME_QUERY: self.folder.name,
                                  FOLDER_PATH_QUERY: self.folder.path
        })
        
        
    
        return query
    
    
    def dumpObject(self, dumpObject):
        import dill as pickle
        
        with open(self.fullpathTranslated(), 'wb') as f:
            pickle.dump(dumpObject, f)
            
            
    def loadObject(self):
        import dill as pickle
        
        with open(self.fullpathTranslated(),'rb') as f:
            loadedObject = pickle.load(f)
                
        return loadedObject




        
    

def fromQuery(query):
    parsedQuery = urlparse.parse_qs(query)
    
    name            =   parsedQuery[NAME_QUERY][0]
    folderName      =   parsedQuery[FOLDER_NAME_QUERY][0]
    folderPath      =   parsedQuery[FOLDER_PATH_QUERY][0]
            
    folder = Folder.Folder(folderName, folderPath)
    newFile = File(name, folder)
    
    return newFile
  
    
    
    
    
def fromFullpath(fullpath):
    folderPath, folderName, fileName = fullpath.rsplit('/', 2)
    
    folder = Folder.Folder(folderName, folderPath)
    newFile = File(fileName, folder)
    
    return newFile

def fromNameAndDir(fileName, dirPath):
    folder = Folder.fromFullpath(dirPath)
    newFile = File(fileName, folder)
    
    return newFile

def fromInvalidNameAndDir(originalName, dirPath):
    import utils
    
    name = utils.createValidName(originalName)
    return fromNameAndDir(name, dirPath) 


def loadObjectFromFP(fullpath):
    dumpFile = fromFullpath(fullpath)
    return dumpFile.loadObject()