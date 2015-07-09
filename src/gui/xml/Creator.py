class Creator(object):
    def __init__(self, posX=0, posY=0, bgColor=0x0000ff, dControl=None, forceDControl=False, 
                 allowOverlay=True, views=None, visible=True, openAnimation=None, closeAnimation=None, 
                 zOrder=1, previousWindow=None, onLoad=None, onUnload=None):
                
        self.posX=posX
        self.posY=posY
        self.bgColor = bgColor
        self.dControl = dControl
        self.forceDControl = forceDControl
        self.allowOverlay = allowOverlay
        self.views = views
        self.visible = visible
        self.openAnimation  = openAnimation
        self.closeAnimation = closeAnimation
        self.zOrder = zOrder
        self.previousWindow = previousWindow
        self.onLoad = onLoad
        self.onUnload = onUnload
        
        
    