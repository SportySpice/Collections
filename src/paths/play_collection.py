from src.collection import loader
from src.li.ItemPlayList import ItemPlaylist
from visual.play_collection import videosVisual


def play(collectionFile):
    collection = loader.load(collectionFile)
    collection.updateVideosIfTime()
    
    
    
    #collection.updateVideoList()  

    
    playlist = ItemPlaylist()
    
    for video in collection.videoList:    
        playlist.addVideo(video, videosVisual, playIfFirst=True)        