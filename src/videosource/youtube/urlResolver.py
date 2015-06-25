import YDStreamExtractor


def resolve(videoId):
    fullUrl = "https://www.youtube.com/watch?v=" + videoId
    vid = YDStreamExtractor.getVideoInfo(fullUrl,quality=1)    
    return vid.streamURL()


def fullInfo(videoId):
    fullUrl = "https://www.youtube.com/watch?v=" + videoId
    vid = YDStreamExtractor.getVideoInfo(fullUrl,quality=1)
    
    streamurl = vid.streamURL()
    title = vid.title
    description = vid.description
    thumb = vid.thumbnail    
    
            
    return streamurl, title, description, thumb








# def batchResolve(collection):
#     for video in collection.videoList:
#         thread = ResolveThread(video)
#         thread.start()
# 
# 
# import threading
# class ResolveThread(threading.Thread):
#     def __init__(self, video):
#         threading.Thread.__init__(self)
#         self.video = video
#         
#     def run(self):       
#         vid = YDStreamExtractor.getVideoInfo(self.video.fullUrl(),quality=1)