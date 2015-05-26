from src.collection import loader
from src.li.ItemPlayList import ItemPlaylist
from visual.play_collection import videosVisual


def play(videoId, sourceId, collectionFile):
    collection = loader.load(collectionFile)
    source = collection.getSource(sourceId)
    playlist = ItemPlaylist()
       
#     for video in collection.videoList:
#         if video.id == videoId:
#             playlist.addVideoAndResolve(video, videosVisual)
#    
#         else:
#             playlist.addVideo(video, videosVisual)


    for video in source.unlimitedVideos():
        playlist.addVideo(video, videosVisual)
        
        if video.id == videoId:
            playlist.playFromLast()
    