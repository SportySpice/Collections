# from src.li.ItemList import ItemList
# from visual.browse_folder import foldersVisual, collectionsVisual, viewStyle
# 
# 
# 
# 
# def browse(folder):
#     items = ItemList()    
#     files, subfolders = folder.listFolder()
#     
#     
#     for subfolder in subfolders:
#         if subfolder.name != "_images":
#             items.addFolder(subfolder, foldersVisual)
#             
# 
#     for collectionFile in files:
#         items.addCollection(collectionFile, collectionsVisual)
#         
#         
#         
#     items.present(viewStyle)