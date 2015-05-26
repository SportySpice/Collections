import xbmcvfs
import xbmc
import File
import urllib
import urlparse


NAME_QUERY = 'folderName'
PATH_QUERY = 'folderPath'



class Folder(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.fullpath = path + '/' + name
        
        self._pathTranslated = None
        self._fullpathTranslated = None
        
        self.fileList = None        
        self.fileDic = None
        self.subfolderList = None
        self.subfolderDic = None
        
        self.listed = False
        
    def exists(self):
        return xbmcvfs.exists(self.fullpath)
    
    def create(self):
        xbmcvfs.mkdirs(self.fullpath)
        
    def createIfNotExists(self):
        if not self.exists():
            self.create()
        
    
    def pathTranslated(self):
        if self._pathTranslated is None:            
            self._pathTranslated = xbmc.translatePath(self.path)
            
        return self._pathTranslated
        
        
        
    def fullpathTranslated(self):        
        if self._fullpathTranslated is None:            
            self._fullpathTranslated = xbmc.translatePath(self.fullpath)
            
        return self._fullpathTranslated
    
    
    
    def listFolder(self):
        if not self.listed:
            fileList = []
            fileDic = {}
            subfolderList = []
            subfolderDic = {}
                        
            subfolderNames, fileNames = xbmcvfs.listdir(self.fullpathTranslated())        
            
            
            
            for subfolderName in subfolderNames:
                subfolder = Folder(subfolderName, self.fullpath)
                subfolderList.append(subfolder)
                subfolderDic[subfolderName] = subfolder
                
                        
            for filename in fileNames:
                newFile = File.File(filename, self)
                fileList.append(newFile)
                fileDic[filename] = newFile
                
            self.fileList = fileList
            self.fileDic = fileDic
            self.subfolderList = subfolderList
            self.subfolderDic = subfolderDic
            
            self.listed = True      
         
            
        return self.fileList, self.subfolderList
    
    
    
    def hasFile(self, name):
        if not self.listed:
            self.listFolder()
        
        if name in self.fileDic:
            return True
        
        return False
    
    
    def getFile(self, name):
        if not self.listed:
            self.listFolder()
                    
        return self.fileDic[name]
        
    
    
    def hasSubfolder(self, name):
        if not self.listed:
            self.listFolder()
         
        if name in self.subfolderDic:
            return True
         
        return False
    
    
    def getSubfolder(self, name):
        if not self.listed:
            self.listFolder()
                     
        return self.subfolderDic[name]
    
    
    
#     def hasSubfolder(self, name):
#         subfolder = Folder(name, self.fullpath)
#         if subfolder.exists():
#             return True
#         
#         return False
#     
#     
#     def getSubfolder(self, name):
#         subfolder = Folder(name, self.fullpath)
#         return subfolder
        
        
    
    
    
    
    
    def encodedQuery(self):
        query = urllib.urlencode({NAME_QUERY: self.name,
                                  PATH_QUERY: self.path
        })
    
        return query
    
    
    
    
def fromQuery(query):
    parsedQuery = urlparse.parse_qs(query)
    
    name = parsedQuery[NAME_QUERY][0]
    path = parsedQuery[PATH_QUERY][0]        
    folder = Folder(name, path)
    
    return folder

    
def fromFullpath(fullpath):
    path, name = fullpath.rsplit('/', 1)
    folder = Folder(name, path)
    
    return folder