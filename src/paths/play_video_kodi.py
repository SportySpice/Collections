from src.tools import videoResolve
from src.videosource.kodi.KodiVideo import watchedDic




def play(path):
    videoResolve.resolve(path)
    watchedDic.videoPlayed(path)