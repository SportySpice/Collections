from visual.browse_youtube_subscriptions import viewStyle, channelsVisual, nextPageVisual
from src.videosource.youtube import login
from src.videosource.youtube import Subscriptions
from src.li.ItemList import ItemList
from src import router

def browse(pageNum=1):
    if not login.hasCredentials():
        import sign_in_out_youtube
        if not sign_in_out_youtube.signIn():
            return
    
    
    subscriptions = Subscriptions.load()
    
    items = ItemList()
    channels = subscriptions.channels
    
    for channel in channels.updatedPageItems(pageNum):
        items.addYoutubeChannel(channel, channelsVisual)
        
    if channels.hasPage(pageNum+1):
        items.addCustomFolder(router.browseYoutubeSubscriptionsUrl(pageNum+1), nextPageVisual(pageNum+1))
        
    items.present(viewStyle)