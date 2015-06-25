import unicodedata

##root node and children need to be ORDERED, not regular ones
def export(rootNode, xmlFile):
    fileStr = _processNode(rootNode)
    
    
    if type(fileStr) is unicode:                    
        fileStr = unicodedata.normalize('NFKD', fileStr).encode('ascii','ignore')
    xmlFile.write(fileStr)
        




def _processSettings(settings):
    settingsStrList = []
    #settingsStr = ''
    
    for setting in settings.list():
        settingStr = setting.key
        
        value = setting.value
        valueType = type(value)
        if valueType is int:
            settingStr += '=%s' %str(value)
                
        elif valueType is bool:
            if value is False:
                settingStr += '=false' 
        elif (valueType is str) or (valueType is unicode) :
            value = value.replace("'", '&%')            
            settingStr += "='%s'" %value
            
        elif value is None:
            settingStr += '=none'
            
        else:
            raise ValueError('Unsupported value type when exporting cxml: {0}'.format(valueType))
        
        settingsStrList.append(settingStr)
    
    settingsStr = ' '.join(settingsStrList)
    return settingsStr


def _processNode(node, indent=0):
    nodeStr = indent*'\t'
    nodeStr += '<' + node.name
    
    if node.hasSettings():
        settingsStr = _processSettings(node.orderedSettings)
        nodeStr += ' ' + settingsStr

    nodeStr += '>' 
    if node.text:
        nodeStr += node.text
    
    if node.children:
        nodeStr += '\n'
        nodeStr += '\n\n'.join(_processNode(child, indent+1) for child in node.children)
    
    for textRow in node.orderedTextRows:
        nodeStr += '\n'
        nodeStr += (indent+1) * '\t'
        nodeStr += _processTextRow(textRow) 
        
    return nodeStr
    
    
def _processTextRow(textRow):
    textRowStr = textRow.text
    
    if textRow.hasSettings():
        settingsStr = _processSettings(textRow.orderedSettings)
        textRowStr += ' < %s>' %settingsStr
        
    if textRow.hasComment():
        textRowStr += '\t\t\t<!--%s-->' %textRow.comment
        
    return textRowStr