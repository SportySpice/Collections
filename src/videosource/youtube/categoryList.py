import service
from settings import regionCode
import Category




def fetch():    
    request = service.service().guideCategories().list(part='snippet', regionCode=regionCode)
    response = request.execute()
    
    categories = []
        
    for item in response['items']:
        category = Category.fromCategoryList(item)
        categories.append(category)
        
    return categories