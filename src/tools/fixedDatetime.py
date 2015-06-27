from datetime import datetime
import time

canUseNormal = True

def strptime(dateStr, formatStr, normalOnly=False):
    global canUseNormal
    
    if canUseNormal:
        try:
            date = datetime.strptime(dateStr, formatStr)
            return date
        
        except TypeError:
            canUseNormal = False
            if normalOnly:
                return
                    
                    
    date = datetime(*(time.strptime(dateStr, formatStr)[:6]))        
    #date = datetime.fromtimestamp(time.mktime(time.strptime(timeStr, format)))        
                
    return date


throwaway = strptime('20110101','%Y%m%d', normalOnly=True)     #seems like this needs to be called in order to
                                                                #prevent some thread error (python bug)