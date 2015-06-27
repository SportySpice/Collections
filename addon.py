import xbmc
import sys
from src import router


sys.path.append(xbmc.translatePath('special://home/addons/plugin.video.collections/src/tools'))

#path = sys.argv[0][34:-1]
#path = sys.argv[0][:-1]
path = sys.argv[0]
query = sys.argv[2][1:]
  
router.route(path, query)






