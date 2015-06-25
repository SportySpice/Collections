import xbmcaddon

xbmcAddon = xbmcaddon.Addon()

def get(settingId, default=None, isInt=False, lower=False, valueList=None):
    setting = xbmcAddon.getSetting(settingId)
    if setting == '':
        return default
    
    if isInt:
        return int(setting)
    
    if valueList:
        setting = int(setting)
        setting = valueList[setting]
    
    if lower:
        return setting.lower()
    
    return setting

def set(settingId, value):
    xbmcAddon.setSetting(settingId, value)


def version():
    return xbmcAddon.getAddonInfo('version')


def string(idNum):
    return xbmcAddon.getLocalizedString(30000 + idNum)