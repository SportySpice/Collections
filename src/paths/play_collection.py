from src.collection import Collection
from src.li.ItemPlayList import ItemPlaylist


def play(collectionFile):
    collection = Collection.fromFile(collectionFile)
    collection.updateDatedSources()

    playlist = ItemPlaylist()
        
    for video in collection.videos:    
        playlist.addVideo(video, collection.feedSettings.TS.videosVisual(), playIfFirst=True)        