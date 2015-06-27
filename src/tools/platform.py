def isAndroid():
    import os                    
    if 'XBMC_ANDROID_APK' in os.environ.data:
        return True     
    
    return False

    #if 'XBMC_ANDROID_LIBS' in os.environ.data:
    #if 'XBMC_ANDROID_SYSTEM_LIBS' in os.environ.data:    
    #if 'linux' in sys.platform: