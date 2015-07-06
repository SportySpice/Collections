from datetime import datetime, timedelta, MINYEAR
from src.tools import pytz
from src.tools.enum import enum





VideoSort = enum (DATE=1, VIEWS=2, DURATION=3, POSITION=4, SHUFFLE=5, SOURCE_TITLE=6, VIDEO_TITLE=7, RATING=8, 
                  LIKES=9, DISLIKES=10, COMMENTS=11, PLAYCOUNT=12, LASTPLAYED=13)

vs = VideoSort
vsToKey = {                                                                                                                                     #reverse
    vs.DATE        :   (lambda video:   video.date                     if video.date        else datetime(MINYEAR, 1, 1, tzinfo=pytz.utc),      True    ),
    vs.VIEWS       :   (lambda video:   video.viewCount                if video.isYoutube() else -1,                                            True    ),
    vs.DURATION    :   (lambda video:   video.duration                 if video.duration    else  timedelta(-1),                                True    ),
    vs.POSITION    :   (lambda video:   video.position,                                                                                         False   ),    
    vs.SOURCE_TITLE:   (lambda video:   video.source.title.lower(),                                                                             False   ),
    vs.VIDEO_TITLE :   (lambda video:   video.title.lower(),                                                                                    False   ),        
    vs.RATING      :   (lambda v:       v.rating                       if v.rating is not None  else -1,                                        True    ),
    vs.LIKES       :   (lambda video:   video.likeCount                if video.isYoutube()     else -1,                                        True    ),
    vs.DISLIKES    :   (lambda video:   video.dislikeCount             if video.isYoutube()     else -1,                                        True    ),
    vs.COMMENTS    :   (lambda video:   video.commentCount             if video.isYoutube()     else -1,                                        True    ),
    vs.PLAYCOUNT   :   (lambda video:   video.playCount(),                                                                                      True    ),
    vs.LASTPLAYED  :   (lambda video:   video.lastPlayed()             if video.lastPlayed() else datetime(MINYEAR, 1, 1),                      True    )
}



VideoCountType = enum (DATE=1, VIEWS=2, DURATION=3, POSITION=4, RATING=5, LIKES=6, DISLIKES=7, 
                       COMMENTS=8, PLAYCOUNT=9, LASTPLAYED=10)


    













class VideoList(object):
    def __init__(self, videos=None, cSources=None, limit=None, unwatchedOnly=False):
        if videos:
            self._videos = videos
            
            
        elif cSources:
            videos = []
            
            if unwatchedOnly:
                for cSource in cSources:
                    for video in cSource.allVideos():
                        videos.appendIfUnwatched(video)
            
            else:            
                for source in cSources:
                    for video in source.allVideos():
                        videos.append(video)
                        
            self._videos = videos
                    
                    
            
            
            
        else:
            self._videos = []
            
        
        self.cSources = cSources
        self.limit = limit
        
        
    def __iter__(self):
        return iter(self._videos)
    
    def __len__(self):
        return len(self._videos)
            
        
    def __getitem__(self, index):
        return self._videos[index]
    

    


    def append(self, video):
        self._videos.append(video)
        
    def appendIfUnwatched(self, video):
        if not video.watched():
            self.append(video)
            

    def sort(self, videoSort, videoSort2=None, reverseOrder=False):
        if videoSort == VideoSort.SHUFFLE:
            from random import shuffle
            shuffle(self._videos)
            return
        
        keyGetter, reverse = vsToKey[videoSort]
        
        if videoSort2:
            keyGetter2 =  vsToKey[videoSort2][0]
            key = lambda video: (keyGetter(video), keyGetter2(video))
             
        else:
            key = lambda video: keyGetter(video)
            
            
        if reverseOrder:
            reverse = not reverse
            
            
        self._videos.sort(None, key=key, reverse=reverse)
    
    
    

    def applyLimits(self):        
        if self.cSources:
            limitedVideos = []            
            
            limitInfoDic = {}
            for cSource in self.cSources:
                limitInfo = LimitInfo(cSource.limit())                
                limitInfoDic[cSource.id] = limitInfo
                
            for video in self._videos:
                limitInfo = limitInfoDic[video.source.id]
                                
                if limitInfo.reachedLimit:
                    continue
                
                limitedVideos.append(video)
                limitInfo.addedItem()
                
            self._videos = limitedVideos
                                                
            
        if self.limit:
            self._videos = self._videos[:self.limit]
        
        
        
        
        
#         limit = self.limit
#         if limit:
#             listLength = len(self._videos)        
#             if listLength > limit:                        
#                 extraItems = listLength - limit
#             del self._videos[-extraItems:]


# ### NOTE: the following 2 methods cache and load all the sources in the wrong way, they can only be used 
# ### to read data such as source title and limit and nothing more. Will have to cache/load sources 
# ### correctly in the future if needing to do more
#     def cache(self, videosVisual):
#         cSources = self.cSources
#         
#         
#         self.videosVisual = videosVisual
#         
#         videoListFile = File.fromInvalidNameAndDir(VIDEO_LIST_FILE, GENERAL_CACHE_DIR)
#         videoListFile.dumpObject(self)
# 
# 
# def loadFromFile():
#     videoListFile = File.fromInvalidNameAndDir(VIDEO_LIST_FILE, GENERAL_CACHE_DIR)
#     return videoListFile.loadObject()




class LimitInfo(object):
    def __init__(self, limit):
        self.limit = limit
        self.itemsAdded = 0
        
        if limit == 0:
            self.reachedLimit = True
        else:
            self.reachedLimit = False
            
    
    def addedItem(self):
        self.itemsAdded += 1
        
        if self.itemsAdded == self.limit:
            self.reachedLimit = True
    
    
    











"""
pretty
 
Formats dates, numbers, etc. in a pretty, human readable format.
"""
 
def _df(seconds, denominator=1, text='', past=True):
    if past:   return         str((seconds + denominator/2)/ denominator) + text #+ ' ago'
    else:      return 'in ' + str((seconds + denominator/2)/ denominator) + text
 
def prettyDate(time=False, asdays=False, short=True):
    '''Returns a pretty formatted date.
    Inputs:
        time is a datetime object or an int timestamp
        asdays is True if you only want to measure days, not seconds
        short is True if you want "1d ago", "2d ago", etc. False if you want
    '''
     
    if time and time.tzinfo:
        now = datetime.now(pytz.utc)
    else:
        now = datetime.now()
     
    if type(time) is int:   time = datetime.fromtimestamp(time)
    elif not time:          time = now
 
    if time > now:  past, diff = False, time - now
    else:           past, diff = True,  now - time
    seconds = diff.seconds
    days    = diff.days
 
    if short:
        if days == 0 and not asdays:
            if   seconds < 10:          text = 'now'            
            elif seconds < 60:          text =  _df(seconds, 1, 's', past)
            elif seconds < 3600:        text =  _df(seconds, 60, 'm', past)
            else:                       text =  _df(seconds, 3600, 'hr', past)

            
        else:
            #if   days   == 0:           tsxt =  'today'
            if days   == 1:             text =  past and 'yest' or 'tom'            
            elif days    < 7:           text =  _df(days, 1, 'd', past)
            elif days    < 31:          text =  _df(days, 7, 'wk', past)
            elif days    < 365:         text =  _df(days, 30, 'mo', past)
            else:                       text =  _df(days, 365, 'yr', past)
        
        return text
            
            
            
    else:
        if days == 0 and not asdays:
            if   seconds < 10:          return 'now'
            elif seconds < 60:          return _df(seconds, 1, ' seconds', past)
            elif seconds < 120:         return past and 'a minute ago' or 'in a minute'
            elif seconds < 3600:        return _df(seconds, 60, ' minutes', past)
            elif seconds < 7200:        return past and 'an hour ago' or'in an hour'
            else:                       return _df(seconds, 3600, ' hours', past)
        else:
            if   days   == 0:           return 'today'
            elif days   == 1:           return past and 'yesterday' or 'tomorrow'
            elif days   == 2:           return past and 'day before' or 'day after'
            elif days    < 7:           return _df(days, 1, ' days', past)
            elif days    < 14:          return past and 'last week' or 'next week'
            elif days    < 31:          return _df(days, 7, ' weeks', past)
            elif days    < 61:          return past and 'last month' or 'next month'
            elif days    < 365:         return _df(days, 30, ' months', past)
            elif days    < 730:         return past and 'last year' or 'next year'
            else:                       return _df(days, 365, ' years', past)




import humanize
def prettyNumber(value, format='%.0f'):
    if value < 1000:
        return '1k'
    
        
    if value >=1000000 and value <=10000000:
        format='%.1f'
            
    return humanize.intword(value, format)
    
    


def prettyNumber2(value, format='%.0f'):        
    #if (value >=1000 and value <=10000) or (value >=1000000 and value <=10000000):
    if value >=1000000 and value <=10000000:
        format='%.1f'
    return humanize.intword(value, format)
    
    


def ratingText(rating):
    if rating is None:
        return None
    
    if rating == 10.0:
        return '10.0'
    
    if rating == 0.0:
        return '0.0' 
    
    return "%.2f" % rating
    
  
    

vct = VideoCountType
vctToText = {                                                                                                   #max chars      text if none (aligned mode only)
    vct.DATE        :   (lambda video:  prettyDate(video.date)          if video.date           else None,      4,              ' '*11  ),
    vct.VIEWS       :   (lambda video:  prettyNumber(video.viewCount)   if video.isYoutube()    else None,      4,              ' '*12  ),    
    vct.DURATION    :   (lambda video:  video.duration                  if video.duration       else None,      None,           ' '*13  ),
    vct.POSITION    :   (lambda video:  video.position                  if video.position       else None,      3,              None    ),
                                                                                                                                       
    vct.RATING      :   (lambda video:  ratingText(video.rating),                                               4,              ' '*10  ),
    vct.LIKES       :   (lambda v:      prettyNumber2(v.likeCount)      if v.isYoutube()        else None,      4,              ' '*12  ),
    vct.DISLIKES    :   (lambda v:      prettyNumber2(v.dislikeCount)   if v.isYoutube()        else None,      4,              ' '*12  ),
    vct.COMMENTS    :   (lambda v:      prettyNumber2(v.commentCount)   if v.isYoutube()        else None,      4,              ' '*12  ),
    vct.PLAYCOUNT   :   (lambda video:  video.playCount(),                                                      3,              None    ),
    vct.LASTPLAYED  :   (lambda video:  prettyDate(video.lastPlayed())  if video.lastPlayed()   else None,      4,              ' '*11  ),
                 
}


vsToCounts = {
    vs.DATE         :   (vct.DATE,      vct.VIEWS),
    vs.VIEWS        :   (vct.VIEWS,     vct.DATE),  
    vs.DURATION     :   (vct.DATE,      vct.VIEWS),
    vs.POSITION     :   (vct.DATE,      vct.VIEWS),
    vs.SHUFFLE      :   (vct.DATE,      vct.VIEWS),
    vs.SOURCE_TITLE :   (vct.DATE,      vct.VIEWS),
    vs.VIDEO_TITLE  :   (vct.DATE,      vct.VIEWS),
    
    vs.RATING       :   (vct.RATING,    vct.DATE),
    vs.LIKES        :   (vct.LIKES,     vct.DATE),
    vs.DISLIKES     :   (vct.DISLIKES,  vct.DATE),
    vs.COMMENTS     :   (vct.COMMENTS,  vct.DATE),
    vs.PLAYCOUNT    :   (vct.PLAYCOUNT, None),
    vs.LASTPLAYED   :   (vct.LASTPLAYED,None)       
}









# import humanize
# def prettyDate(value, future=False, months=True):
#     return humanize.naturaltime(value, future, months)








# def prettyDate(time=False):
#     """
#     Get a datetime object or a int() Epoch timestamp and return a
#     pretty string like 'an hour ago', 'Yesterday', '3 months ago',
#     'just now', etc
#     """
#     from datetime import datetime
#     now = datetime.now()
#     if type(time) is int:
#         diff = now - datetime.fromtimestamp(time)
#     elif isinstance(time,datetime):
#         diff = now - time
#     elif not time:
#         diff = now - now
#     second_diff = diff.seconds
#     day_diff = diff.days
# 
#     if day_diff < 0:
#         return ''
# 
#     if day_diff == 0:
#         if second_diff < 10:
#             return "just now"
#         if second_diff < 60:
#             return str(second_diff) + " seconds ago"
#         if second_diff < 120:
#             return "a minute ago"
#         if second_diff < 3600:
#             return str(second_diff / 60) + " minutes ago"
#         if second_diff < 7200:
#             return "an hour ago"
#         if second_diff < 86400:
#             return str(second_diff / 3600) + " hours ago"
#     if day_diff == 1:
#         return "Yesterday"
#     if day_diff < 7:
#         return str(day_diff) + " days ago"
#     if day_diff < 31:
#         return str(day_diff / 7) + " weeks ago"
#     if day_diff < 365:
#         return str(day_diff / 30) + " months ago"
#     return str(day_diff / 365) + " years ago"



# import math
# millnames=['','Thousand','Million','Billion','Trillion']
# def prettyNumber(n):
#     n = float(n)
#     millidx=max(0,min(len(millnames)-1,
#                       int(math.floor(math.log10(abs(n))/3))))
#     return '%.0f %s'%(n/10**(3*millidx),millnames[millidx])







# def intWithCommas(number):
#     if type(number) not in [type(0), type(0L)]:
#         raise TypeError("Parameter must be an integer.")
#     if number < 0:
#         return '-' + intWithCommas(-number)
#     result = ''
#     while number >= 1000:
#         number, r = divmod(number, 1000)
#         result = ",%03d%s" % (r, result)
#     return "%d%s" % (number, result)



# def inWithCommas(number):
#     return humanize.intcomma(number)


# def intWithCommas2(number):
#     s = '%d' % number
#     groups = []
#     while s and s[-1].isdigit():
#         groups.append(s[-3:])
#         s = s[:-3]
#     return s + ','.join(reversed(groups))


#def intWithCommas3(number)
    #return'{:,}'.format(number)    # only works on python 2.7+













#     def __setitem__(self, index, value):
#         self._videos[index] = value
#         
#     def __delitem__(self, index):
#         del self._videos[index]








# def _date           (video):    return video.date           if video.date        else datetime(MINYEAR, 1, 1, tzinfo=pytz.utc)
# def _views          (video):    return video.viewCount      if video.isYoutube() else -1    
# def _sourceTitle    (video):    return video.source.title
# def _videoTitle     (video):    return video.title
# def _Duration       (video):    return video.duration
# def _position       (video):    return video.position
# def _rating         (video):    return video.rating    
# def _likes          (video):    return video.likeCount      if video.isYoutube() else -1
# def _dislikes       (video):    return video.dislikeCount   if video.isYoutube() else -1    
# def _commentCount   (video):    return video.commentCount   if video.isYoutube() else -1
# def _playCount      (video):    return video.playCount()
# def _lastPlayed     (video):    return video.lastPlayed()