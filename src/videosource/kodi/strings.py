import simplejson as json
    
    #unused =     "fanart", "studio", "sorttitle","season","episode", "genre", "tagline", "plotoutline", "album","artist","showtitle","description","duration"
        
DESCRIPTION_PROPS = '"title","plot"'
IMAGE_PROPS =  '"thumbnail"'   
DATE_PROPS  =  '"firstaired","premiered","dateadded","year"'
PLAY_PROPS = '"runtime","playcount","lastplayed"'
OTHER_PROPS = '"rating"'

PROPS =  ','.join([DESCRIPTION_PROPS, IMAGE_PROPS, DATE_PROPS, PLAY_PROPS, OTHER_PROPS])




def jsonRpcDir(path, mediaType):
    path = json.dumps(path)
    jsonStr = '{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory": %s, "media": "%s", "properties":[%s]}, "id": 1}' % (path, mediaType, PROPS)
    return jsonStr


def jsonRpcFile(path, mediaType):
    json = '{"jsonrpc": "2.0", "method": "Files.GetFileDetails", "params": {"file": "%s", "media": "%s", "properties":[%s]}, "id": 2}' % (path, mediaType, PROPS)
    return json