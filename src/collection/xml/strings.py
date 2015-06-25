from src.collection.Collection import OnCollectionClick as occ
from src.collection.CollectionSource import OnSourceClick as osc
from src.videosource.Video import OnVideoClick as ovc
from src.li.visual.CountTextSettings import CountType as ct
from src.li.visual.CountTextSettings import Location as loc


#enum conversions
occToValue  =   {None:None,     occ.FEED:'feed',    occ.SOURCES:'sources',      occ.SOURCES_ONLY:'sourcesOnly',     occ.PLAYALL:'playAll'}
valueToOcc  =   {None:None,     'feed':occ.FEED,    'sources':occ.SOURCES,      'sourcesOnly':occ.SOURCES_ONLY,     'playAll':occ.PLAYALL}

oscToValue  =   {None:None,     osc.BROWSE:'browse',   osc.PLAYALL:'playAll',      osc.BROWSE_ORIGIN:'browseOrigin'}
valueToOsc  =   {None:None,     'browse':osc.BROWSE,   'playAll':osc.PLAYALL,      'browseOrigin':osc.BROWSE_ORIGIN}

ovcToValue  =   {ovc.PLAY_ONLY:'playOnly',      ovc.PLAY_QUEUE_REST:'playQueue'}
valueToOvc  =   {'playOnly':ovc.PLAY_ONLY,      'playQueue':ovc.PLAY_QUEUE_REST}


locToValue  =   {loc.LEFT:'left',   loc.MIDDLE:'middle',    loc.RIGHT:'right'}
valueToLoc  =   {'left':loc.LEFT,   'middle':loc.MIDDLE,    'right':loc.RIGHT}

ctToValue   =   {ct.VIEWS:'views',  ct.SUBSCRIBERS:'subscribers',   ct.VIDEOS:'videos',     ct.NEW_VIDEOS:'newVideos'}
valueToCt   =   {'views':ct.VIEWS,  'subscribers':ct.SUBSCRIBERS,   'videos':ct.VIDEOS,     'newVideos':ct.NEW_VIDEOS}









#strings used in multiple places
ON_CLICK            = 'onClick'
VIEWSTYLE           = 'viewStyle'
USE                 = 'use'
USETS               = 'useTS'

#TS
TS_COLOR            = 'color'
TS_BOLD             = 'bold'
TS_ITALIC           = 'italic'
TS_SHOW             = 'show'

CTS_LOACTION        = 'location'
CTS_TYPE            = 'countType'




#collection
COLLECTION_NODE     = 'collection'
COLLECTION_DEFAULT  = 'default'


#views
VIEWS_NODE              = 'views'


#feed
FEED_NODE               = 'feed'
FEED_VIDEOCLICK         = 'videoClick'
FEED_UNWATCHED          = 'unwatched'
FEED_LIMIT              = 'limit'
FEED_SLIMIT             = 'sLimit'

FEED_TR_BROWSE_SOURCES  = 'browseSources'
FEED_TR_SETTINGS        = 'settings'
FEED_TR_PLAYALL         = 'playAll'
FEED_TR_VIDEO_COUNT     = 'video_count'
FEED_TR_VIDEO_SOURCE    = 'video_source'
FEED_TR_VIDEO_TITLE     = 'video_title'
    

#sources
SOURCES_NODE                = 'sources'
SOURCES_SOURCE_CLICK_KODI   = 'sourceClickKodi'
SOURCES_SOURCE_CLICK_YT     = 'sourceClickYt'

SOURCES_TR_CSOURCE          = 'source'    

    


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