from src.videosource.Video import Video
from datetime import datetime, timedelta
from src.tools import fixedDatetime
from src import router
from src.tools import WatchedDic
from src.paths.root import KODI_DATA_DIR
from src.tools import pytz




WATCHED_DIC_FILE           = 'watched.dic'
watchedDic = WatchedDic.load(WATCHED_DIC_FILE, KODI_DATA_DIR)


class KodiVideo(Video):
    def __init__(self, kodiFolder, position, item):
        title               =       _processTitle(item)        
        description         =       _getValue(item, 'plot')
        thumb               =       _getValue(item, 'thumbnail')
        
        path                =       item['file']
        self.path = path
        videoId = path
        
        date            =       _processDate(item)
        duration        =       _processDuration(item)
        #playCount      =       _getValue(item, 'playcount')
        #lastPlayed     =       _processLastPlayed(item)
        
        rating          =       item.get('rating', 0)



        super(KodiVideo, self).__init__(videoId, kodiFolder, position, title, description, thumb, date, duration, rating)
        


    #override
    def playUrl(self):
        return router.playVideoKodiUrl(self.path)

        


    
    def isKodiVideo(self):
        return True
        
    def isKodiFolder(self):
        return False
    
    
    def watched(self):
        return watchedDic.watched(self.path)
        

    def watchedInfo(self):
        return watchedDic.info(self.path)










####################
## Private Methods##
####################
def _processTitle(item):
    if item['label'] != '':
        return item['label']
    
    if item['title'] != '':
        return item['title']
    
    return ''
        
        
        
def _processDate(item):
    date = None
    
    if _getValue(item, 'firstaired'):
        date = item['firstaired']
    elif _getValue(item, 'premiered'):
        date = item['premiered']
    elif _getValue(item, 'dateadded'):
        date = item['dateadded']
        
    if date is not None:
        date = fixedDatetime.strptime(date, '%Y-%m-%d')
        date = pytz.UTC.localize(date)
        return date
        
    
    if _getValue(item, 'year'):
        year = item['year']
        return datetime(year=year, month=1, day=1, tzinfo=pytz.UTC)
            
        
    return None



def _processDuration(item):
    if _getValue(item, 'runtime'):
        duration = timedelta(seconds = item['runtime'])
        return duration
    
    return None


def _processLastPlayed(item):
    if _getValue(item, 'lastplayed'):
        lastplayed = fixedDatetime.strptime(item['lastplayed'], '%Y-%m-%d %H:%M:%S')
        return lastplayed
    
    return None






def _getValue(item, key):
    if key in item:
        if item[key] != '': 
            return item[key]
    
    return None