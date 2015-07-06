from src.li import ItemPlayList

def play(videoIndex=0):    
    playlist = ItemPlayList.loadFromFile()
    
    
    playlist.playFrom(videoIndex)
    
    
    
       
#     for video in collection.videoList:
#         if video.id == videoId:
#             playlist.addVideoAndResolve(video, videosVisual)
#    
#         else:
#             playlist.addVideo(video, videosVisual)
    
    

