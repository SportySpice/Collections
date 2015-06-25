from src.file import File
from src.collection import Collection
from src.tools.dialog import dialog
from visual.create_new_collection import NAME_INPUT_HEADING, successDialog


def create(dirPath, showSuccessDialog=True):
    title = dialog.input(NAME_INPUT_HEADING)
    title = title.strip()
    
    if not title:
        return False
    
    collection = Collection.emptyFromDirPath(title, dirPath)    
    collection.writeCollectionFile()
    
    if showSuccessDialog:
        successDialog(collection)
    
    return collection