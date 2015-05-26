from apiclient.discovery import build


DEVELOPER_KEY = "AIzaSyCtyf8jToJowBEhpNL37UU3EjW0QhowXc4"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

_service = None

def service():    
    global _service
    
    if _service is None:
        _service = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        
        
    return _service