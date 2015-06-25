from Node import Node
from TextRow import TextRow
import shlex




def load(xmlFile, rootOnly=False):
    lines = xmlFile.lines()
    
    root =  _processNodeLine(lines[0])
    
    if rootOnly:
        return root
    
    
    children = []
    for i in range(1, len(lines)):                
        line = lines[i]
        line = line.strip()
                
        if line != '':
            
            if line[0] == '<':
                if line != '</>' and line[1] != '!':
                    currentChild = _processNodeLine(line)
                    children.append(currentChild)
            else:
                textRow = _processTextLine(line)
                currentChild.addTextRow(textRow)                 
        
    
    root.children = children
        
    return root


        
        
        
####################
## Private Methods##
####################
def _processSettings(settingsStr):
    settings = {}    
    settingsList = shlex.split(settingsStr)
            
    for setting in settingsList:    
        if '=' in setting:
            key,value = setting.split('=')            
            
            if value.isdigit():
                value = int(value)
                
            elif value=='true':                         #boolean values
                value = True
            
            elif value=='false':
                value = False
                
            elif value=='none':
                value = None
                
            else:            
                value = value.replace('&%', "'")
                
        else:
            key = setting
            value = True
                            
        settings[key] = value
        
    return settings




def _processNodeLine(line):
    nameAndSettings, text = line.split('>', 1)
     
    nameAndSettings = nameAndSettings[1:]    
    if ' ' in nameAndSettings:
        name, settingsStr = nameAndSettings.split(None, 1)         
        settings = _processSettings(settingsStr)     
    else:
        name = nameAndSettings
        settings = {}
        
    
    text = text.split('<!--', 1)[0]
    text=text.strip()

    
    node = Node(name, settings, text)    
    return node


def _processTextLine(line):    
    line = line.split('<!--', 1)[0]
    
    
    if '<' in line:
        text, settingsStr = line.split('<')        
        settingsStr = settingsStr.strip()[:-1]        
        settings = _processSettings(settingsStr)
                
    else:
        text = line
        settings = {}
        
    text = text.strip()
    
    textRow = TextRow(text, settings)
    return textRow
        