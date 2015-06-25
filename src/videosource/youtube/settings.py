from regionCodes import regionCodes
from src.tools import addonSettings
from Thumb import ThumbRes





region          =   addonSettings.get('yt_region', default='United States of America')
regionCode      =   regionCodes[region]

videoThumbres   =   addonSettings.get('yt_video_thumbres', default=ThumbRes.MEDIUM,     isInt=True)
sourceThumbres  =   addonSettings.get('yt_source_thumbres', default=ThumbRes.MEDIUM,    isInt=True)


def subscriptionSorting():
    from  Subscriptions import SubscriptionSorting as ss
    SS_VALUES = (ss.ALPHABETICAL, ss.RELEVANCE, ss.UNREAD)
    _subscriptionSorting = addonSettings.get('yt_subscriptions_sorting', default=ss.ALPHABETICAL, valueList=SS_VALUES)
    
    return _subscriptionSorting




def videosCacheTime():                  return addonSettings.get('yt_videos_cache_time',               default=5,    isInt=True)    #in minutes
def channelPlaylistsCacheTime():        return addonSettings.get('yt_channel_playlists_cache_time',    default=1,    isInt=True)    #in days
def subscriptionChannelsCacheTime():    return addonSettings.get('yt_subscription_channels_cache_time',default=1,    isInt=True)    #in days
def categoryChannelsCacheTime():        return addonSettings.get('yt_category_channels_cache_time',    default=1,    isInt=True)    #in days
def searchesCacheTime():                return addonSettings.get('yt_searches_cache_time',             default=5,    isInt=True)    #in minutes

def sourceInfoCacheTime():              return addonSettings.get('yt_source_info_cache_time',          default=7,    isInt=True)    #in days


# videoDescriptionStats =         addonSettings.get('yt_video_description_stats')
# channelDescriptionStats =         addonSettings.get('yt_channel_description_stats')
# playlistDescriptionStats =         addonSettings.get('yt_playlist_description_stats')