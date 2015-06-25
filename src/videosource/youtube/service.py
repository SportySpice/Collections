from apiclient.discovery import build
import httplib2
import login



DEVELOPER_KEY = "AIzaSyCtyf8jToJowBEhpNL37UU3EjW0QhowXc4"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

_publicService = None
_authedService = None


def service():
    if _authedService:
        return _authedService
    
    if login.hasCredentials():
        buildAuthedService()
        return _authedService
    
    
    if _publicService:
        return _publicService
    
    buildPublicService()
    return _publicService
     





def buildPublicService():    
    global _publicService
    
    _publicService = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)






def buildAuthedService():
    global _authedService
    
    credentials = login.getCredentials()
    
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    _authedService = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=http)