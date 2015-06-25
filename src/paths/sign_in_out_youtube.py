from visual.sign_in_out_youtube import signOutDialog, signOutSuccessDialog, signInDialog, codeDialog, signInSuccessDialog
from src.videosource.youtube import login

def sign():
    if login.hasCredentials():
        if signOutDialog():
            login.signOut()
            signOutSuccessDialog()
        
    else:
        signIn()


    
    




AUTHORIZE_LINK = 'https://accounts.google.com/o/oauth2/device/usercode'

    
def signIn(showSuccessDialog=True):
    import xbmc
        
    
    selection = signInDialog()

    if selection==-1:
        return False

    
    if selection==0:
        import webbrowser
        webbrowser.open_new(AUTHORIZE_LINK)
        
    code = login.fetchSignInInfo()
    cd = codeDialog(code)
    
    while login.tryFetchingCredentials() is False:
        xbmc.sleep(5000)
        if cd.iscanceled():
            cd.close()
            return False
        
        
    cd.close()
    if showSuccessDialog:
        signInSuccessDialog()
    return True