from src.videosource.youtube import categoryList
from src.li.ItemList import ItemList
from visual.browse_youtube_categories import viewStyle, categoriesVisual




def browse():    
    categories = categoryList.fetch()    
    items = ItemList()
        
    for category in categories:
        items.addYoutubeCategory(category, categoriesVisual)
        
        
    items.present(viewStyle)