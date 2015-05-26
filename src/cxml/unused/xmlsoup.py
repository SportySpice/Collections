from bs4 import BeautifulSoup
import Enum

AttribType = Enum.enum(STRING=0, INT=1, BOOL=2)





#returns the root of the file
def root(xmlFile):
    soup =  BeautifulSoup(xmlFile.contents())   
    root = soup.contents[0]
    
        
    root.file = xmlFile     #need to have reference back to the file    
            
    return root
        

#returns all the roots of all the files in a given folder
def rootsAndSubfolders(xmlFolder):
    roots = []
    
    xmlFiles, subfolders = xmlFolder.listFolder()    
    for xmlFile in xmlFiles:
        fileRoot = root(xmlFile)
        roots.append(fileRoot)
        
    return roots, subfolders
    
        
        
                
def getAttrib(attribs, attrib, default, attribType=AttribType.STRING):
    value = attribs.get(attrib)
    if value is None:
        return default
    
    if attribType == AttribType.STRING:
        return value
    
    if attribType == AttribType.INT:        
        return int(value)
    
    if attribType == AttribType.BOOL:
        if value == 'true':
            return True
        elif value == 'false':
            return False
        raise ValueError('Invalid setting for attrib: ' + attrib + '. Value must be "true" or "false"')
        
    raise ValueError('Invalid attribType given for attrib: ' + attrib )