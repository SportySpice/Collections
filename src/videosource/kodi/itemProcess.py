from datetime import datetime, timedelta
from src.tools import fixedDatetime
from src.tools import pytz
from src.tools.enum import enum


DateType = enum ( FIRST_AIRED=1, PREMIERED=2, DATE_ADDED=3, YEAR=4, ESTIMATED=5)




def processAll(item, folderRecord=None):
        path                =       item['file']
    
        title               =       processTitle(item)        
        description         =       _getValue(item, 'plot')
        thumb               =       _getValue(item, 'thumbnail')
        
        

        date, dateType  =       processDate(item, path, folderRecord)
        duration        =       processDuration(item)
        #playCount      =       _getValue(item, 'playcount')
        #lastPlayed     =       _processLastPlayed(item)
        
        rating          =       item.get('rating')      #this returns 0 if empty, can maybe set it as None 
                                                        #when this happens instead of storing the 0
        
        return path, title, description, thumb, date, dateType, duration, rating



def processTitle(item):
    label = item.get('label')
    if label:
        return label
    
    title = item.get('title') 
    if title:
        return title
    
    return ''
        

dt = DateType
valueToDt = {'firstaired':dt.FIRST_AIRED, 'premiered':dt.PREMIERED, 'dateadded':dt.DATE_ADDED, 'year:':dt.YEAR}

def processDate(item, videoId, folderRecord=None):
    date = None
    
    for value in ('firstaired', 'premiered', 'dateadded'):
        date = item.get(value)
        if date:
            date = fixedDatetime.strptime(date, '%Y-%m-%d')
            date = pytz.UTC.localize(date)
            dateType = valueToDt[value]
            
            return date, dateType
        
    
    year = item.get('year')
    if year:     
        if folderRecord:
            date = folderRecord.getEstimation(videoId)
            if date:
                dateType = DateType.ESTIMATED
                return date, dateType
                               
        date = datetime(year=year, month=1, day=1, tzinfo=pytz.UTC)                                             #estimate to get more accurate dates            
        dateType = DateType.YEAR                          
        return date, dateType
          
    
    if folderRecord:
        date = folderRecord.getEstimation(videoId)
        dateType = DateType.ESTIMATED
        return date, dateType
            
        
    return None, None



def processDuration(item):
    duration = item.get('runtime')
    if duration:
        duration = timedelta(seconds=duration) 
        return duration
    
    return None


def processLastPlayed(item):
    lastPlayed = item.get('lastplayed') 
    if lastPlayed:
        lastplayed = fixedDatetime.strptime(lastPlayed, '%Y-%m-%d %H:%M:%S')
        return lastplayed
    
    return None







def _getValue(item, key):
    value = item.get(key)               #note: key can exist in dic with value '',
    return value if value else None     #this is why this check is needed 
                                        