import sys
from src import router

#path = sys.argv[0][34:-1]
#path = sys.argv[0][:-1]
path = sys.argv[0]
query = sys.argv[2][1:]

  
router.route(path, query)