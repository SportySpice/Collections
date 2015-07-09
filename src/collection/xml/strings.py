from src.collection.Collection import OnCollectionClick as occ
from src.collection.CollectionSource import OnSourceClick as osc
from src.videosource.Video import OnVideoClick as ovc
from src.videosource.VideoList import VideoSort as vsr
from src.videosource.VideoList import VideoCountType as vct
from src.li.visual.FullTextSettings import Location as loc


#enum conversions
occToValue  =   {None:None,     occ.FEED:'feed',    occ.SOURCES:'sources',      occ.SOURCES_ONLY:'sourcesOnly',     occ.PLAYALL:'playAll'}
valueToOcc  =   {None:None,     'feed':occ.FEED,    'sources':occ.SOURCES,      'sourcesOnly':occ.SOURCES_ONLY,     'playAll':occ.PLAYALL}

oscToValue  =   {None:None,     osc.BROWSE:'browse',   osc.PLAYALL:'playAll',      osc.BROWSE_ORIGIN:'browseOrigin'}
valueToOsc  =   {None:None,     'browse':osc.BROWSE,   'playAll':osc.PLAYALL,      'browseOrigin':osc.BROWSE_ORIGIN}

ovcToValue  =   {ovc.PLAY_ONLY:'playOnly',      ovc.PLAY_QUEUE_REST:'playQueue'}
valueToOvc  =   {'playOnly':ovc.PLAY_ONLY,      'playQueue':ovc.PLAY_QUEUE_REST}

vsrToValue =   {vsr.DATE:'date',   vsr.VIEWS:'views',       vsr.DURATION:'duration',    vsr.POSITION:'position',    vsr.SHUFFLE:'shuffle',  vsr.SOURCE_TITLE:'sTitle',      vsr.VIDEO_TITLE:'vTitle',       vsr.RATING:'rating',    vsr.LIKES:'likes',  vsr.DISLIKES:'dislikes',    vsr.COMMENTS:'comments',        vsr.PLAYCOUNT:'playCount',  vsr.LASTPLAYED:'lastPlayed'}
valueTovsr =   {'date':vsr.DATE,   'views':vsr.VIEWS,       'duration':vsr.DURATION,    'position':vsr.POSITION,    'shuffle':vsr.SHUFFLE,  'sTitle':vsr.SOURCE_TITLE,      'vTitle':vsr.VIDEO_TITLE,       'rating':vsr.RATING,    'likes':vsr.LIKES,  'dislikes':vsr.DISLIKES,    'comments':vsr.COMMENTS,        'playCount':vsr.PLAYCOUNT,  'lastPlayed':vsr.LASTPLAYED}

vctToValue = {vct.DATE:'date',  vct.VIEWS:'views',    vct.DURATION:'duration',    vct.POSITION:'position',    vct.RATING:'rating',    vct.LIKES:'likes',  vct.DISLIKES:'dislikes',  vct.COMMENTS:'comments',    vct.PLAYCOUNT:'playCount',  vct.LASTPLAYED:'lastPlayed'}
valueToVct = {'date':vct.DATE,  'views':vct.VIEWS,    'duration':vct.DURATION,    'position':vct.POSITION,   'rating':vct.RATING,    'likes':vct.LIKES,  'dislikes':vct.DISLIKES,   'comments':vct.COMMENTS,     'playCount':vct.PLAYCOUNT,  'lastPlayed':vct.LASTPLAYED}



locToValue  =   {loc.LEFT_ALIGNED:'leftAligned',    loc.LEFT:'left',   loc.MIDDLE:'middle',    loc.RIGHT:'right'}
valueToLoc  =   {'leftAligned':loc.LEFT_ALIGNED,    'left':loc.LEFT,   'middle':loc.MIDDLE,    'right':loc.RIGHT}

#ctToValue   =   {ct.VIEWS:'views',  ct.SUBSCRIBERS:'subscribers',   ct.VIDEOS:'videos',     ct.NEW_VIDEOS:'newVideos'}
#valueToCt   =   {'views':ct.VIEWS,  'subscribers':ct.SUBSCRIBERS,   'videos':ct.VIDEOS,     'newVideos':ct.NEW_VIDEOS}









#strings used in multiple places
ON_CLICK            = 'onClick'
VIEWSTYLE           = 'viewStyle'
USE                 = 'use'
USELIMITS          = 'useLimits'
USETS               = 'useTS'

#TS
TS_COLOR            = 'color'
TS_BOLD             = 'bold'
TS_ITALIC           = 'italic'
TS_SHOW             = 'show'

COUNT_LOACTION        = 'countLocation'
#CTS_TYPE            = 'countType'




#collection
COLLECTION_NODE     = 'collection'
COLLECTION_DEFAULT  = 'default'


#views
VIEWS_NODE              = 'views'


#feed settings
FEED_NODE               = 'feed'
FEED_SORT               = 'sort'
FEED_SORT2              = 'sort2'
FEED_REVSORT            = 'reverseSort'
FEED_COUNT_TYPE         = 'countType'
FEED_COUNT_TYPE2        = 'countType2'
#FEED_REPVIEWS           = 'replaceViews'
FEED_VIDEOCLICK         = 'videoClick'
FEED_UNWATCHED          = 'unwatched'
FEED_LIMIT              = 'limit'
FEED_SLIMIT             = 'sLimit'

FEED_TR_BROWSE_SOURCES  = 'browseSources'
FEED_TR_SETTINGS        = 'settings'
FEED_TR_SORT            = 'sort'
FEED_TR_PLAYALL         = 'playAll'
FEED_TR_VIDEO_COUNT     = 'video_count'
FEED_TR_VIDEO_COUNT2    = 'video_count2'
FEED_TR_VIDEO_SOURCE    = 'video_source'
FEED_TR_VIDEO_TITLE     = 'video_title'
    

#sources settings
SOURCES_NODE                = 'sources'
SOURCES_SOURCE_CLICK_KODI   = 'sourceClickKodi'
SOURCES_SOURCE_CLICK_YT     = 'sourceClickYt'

SOURCES_TR_CSOURCE          = 'source'


#folder settings
FOLDERS_SETTINGS_NODE       = 'folderSettings'
FOLDERS_SETTINGS_ESTIMATE   = 'estimateDates'

 

    


#cSource
CSOURCE_LIMIT           = 'limit'
CSOURCE_CUSTOM_TITLE    = 'title'
CSOURCE_CUSTOM_THUMB    = 'thumb'




#channels
CHANNELS_NODE           = 'channels'
CHANNEL_ID              = 'id'

#playlists
PLAYLISTS_NODE          = 'playlists'


#kodiFolders
FOLDERS_NODE            = 'folders'
FOLDER_ESTIMATE_DATES   = 'estimateDates'