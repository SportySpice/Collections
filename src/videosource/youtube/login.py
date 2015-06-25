from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from src.file import File
from oauth2client.file import Storage
from src.paths.root import YOUTUBE_DATA_DIR


CREDENTIALS_FILE = 'credentials' 
ranInit = False
credentials = None


def init():
    global credentials
    global ranInit
    
    if ranInit:
        return
    
    credentialsFile = File.fromNameAndDir(CREDENTIALS_FILE, YOUTUBE_DATA_DIR)
    
    if credentialsFile.exists():
        storage = Storage(credentialsFile.fullpathTranslated())
        credentials = storage.get()
        if credentials and credentials.invalid:
            credentials = None
                        
    else:
        credentials = None

    ranInit = True



def hasCredentials():
    init()
        
    if credentials:
        return True
    
    return False

    

def getCredentials():
    return credentials





def signOut():
    global credentials
    
    credentialsFile = File.fromNameAndDir(CREDENTIALS_FILE, YOUTUBE_DATA_DIR)
    credentialsFile.deleteIfExists()
    credentials = None
        










CLIENT_SECRET_FILE  = 'special://home/addons/plugin.video.collections/src/videosource/youtube/cs'
READ_WRITE_SCOPE    = 'https://www.googleapis.com/auth/youtube'

flow = None
deviceFlowInfo = None


## returns a code for the user to put in his browser and confirm access
def fetchSignInInfo():
    global flow 
    global deviceFlowInfo
    
    clientSecret = File.fromFullpath(CLIENT_SECRET_FILE)
    flow = flow_from_clientsecrets(clientSecret.fullpathTranslated(), scope=READ_WRITE_SCOPE)

    deviceFlowInfo = flow.step1_get_device_and_user_codes()
    code = deviceFlowInfo[1]
    
    return code





#call this at an interval after calling fetchSignInInfo() 
#to check if there user confirmed access
def tryFetchingCredentials():
    global credentials
    
    try:
        credentials = flow.step2_exchange(device_flow_info=deviceFlowInfo)
    except FlowExchangeError as e:
        if e.message != 'authorization_pending':
            raise ValueError ('Unknown FlowExchange error: %s' %e.message)
        
        return False        
    
    if credentials.invalid:
        credentials = None
        return False
    
    credentialsFile = File.fromNameAndDir(CREDENTIALS_FILE, YOUTUBE_DATA_DIR)
    
    storage = Storage(credentialsFile.fullpathTranslated())     #store on hard drive
    storage.put(credentials)
        
    return True


    

    
















#READ_ONLY_SCOPE    = 'https://www.googleapis.com/auth/youtube.readonly'
#REDIERCT_URI        = 'urn:ietf:wg:oauth:2.0:oob'

#directLink = flow.step1_get_authorize_url()


#from oauth2client.client import OAuth2WebServerFlow    
#CLIENT_ID = '1074802623980-dpf5kf1o0e14hkjb9al8st51r2fqk71l.apps.googleusercontent.com'
#CLIENT_SECRET = 'xCvTxLTqi0TbkWijXxYBS8_7'
#     flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
#                            client_secret=CLIENT_SECRET,
#                            scope=READ_WRITE_SCOPE,
#                            redirect_uri=REDIERCT_URI)