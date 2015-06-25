from src.videosource.youtube import urlResolver
from src.videosource.youtube.YoutubeVideo import watchedDic
from src.tools import videoResolve



def play(videoId):
    url = urlResolver.resolve(videoId)    
    videoResolve.resolve(url)
    
    watchedDic.videoPlayed(videoId)