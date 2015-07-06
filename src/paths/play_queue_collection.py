from src.collection import Collection
from src.li.ItemPlayList import ItemPlaylist


def play(videoId, collectionFile):
    collection = Collection.fromFile(collectionFile)
    collection.createCombinedList()   #not bad for now, might wanna cache collection in future
    
    playlist = ItemPlaylist()
    
    
    
    for video in collection.videos:
        playlist.addVideo(video, collection.feedSettings.TS.videosVisual())
        
        if video.id == videoId:
            playlist.playFromLast()
    
    
      
#     for video in collection.videoList:
#         if video.id == videoId:
#             playlist.addVideoAndResolve(video, videosVisual)
#    
#         else:
#             playlist.addVideo(video, videosVisual)
    
    

