import threading

def contentsUpdate(kodiFolders, forceUpdate=False):
    threads = []
    
    for kodiFolder in kodiFolders:
        if forceUpdate or kodiFolder.contentsNeedUpdate():
            thread = kodiFolder.updateContentsThread()
            thread.start()
            threads.append(thread)
            

            
    for thread in threads:
        thread.join()
    
    
    
def contentsUpdateThread(kodiFolders, forceUpdate=False):
    return ContentsUpdater(kodiFolders, forceUpdate)
    
    
    
    
class ContentsUpdater(threading.Thread):
    def __init__(self, kodiFolders, forceUpdate=False):
        threading.Thread.__init__(self)
        self.kodiFolders = kodiFolders
        self.forceUpdate = forceUpdate
        
    def run(self):
        contentsUpdate(self.kodiFolders, self.forceUpdate)