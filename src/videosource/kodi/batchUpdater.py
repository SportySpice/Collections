import threading

def contentsUpdate(kodiFolders, estimateDatesList=None, forceUpdate=False):
    threads = []
    
    index = 0
    for kodiFolder in kodiFolders:
        if forceUpdate or kodiFolder.contentsNeedUpdate():
            estimateDate = estimateDatesList[index] if estimateDatesList else False
            thread = kodiFolder.updateContentsThread(estimateDate)
                
            thread.start()
            threads.append(thread)
            
        index += 1
            

            
    for thread in threads:
        thread.join()
    
    
    
def contentsUpdateThread(kodiFolders, estimateDatesList=None, forceUpdate=False):
    return ContentsUpdater(kodiFolders, estimateDatesList, forceUpdate)
    
    
    
    
class ContentsUpdater(threading.Thread):
    def __init__(self, kodiFolders, estimateDatesList=None, forceUpdate=False):
        threading.Thread.__init__(self)
        self.kodiFolders = kodiFolders
        self.estimateDatesList = estimateDatesList
        self.forceUpdate = forceUpdate
        
    def run(self):
        contentsUpdate(self.kodiFolders, self.estimateDatesList, self.forceUpdate)