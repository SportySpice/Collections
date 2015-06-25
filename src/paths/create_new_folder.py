from src.file import utils
from src.file.Folder import Folder
from src.tools.dialog import dialog
from visual.create_new_folder import NAME_INPUT_HEADING, INVALID_NAME_DIALOG, FOLDER_EXISTS_DIALOG, successDialog


def create(dirPath, showSuccessDialog=True):
    name = dialog.input(NAME_INPUT_HEADING)
    name = name.strip()
    
    if not name:
        return False
    
    if not utils.isNameValid(name):
        dialog.ok(*INVALID_NAME_DIALOG)
        return False
        
    folder = Folder(name, dirPath)
    if folder.exists():
        dialog.ok(*FOLDER_EXISTS_DIALOG)
        return False
    
    
    folder.create()
    
    if showSuccessDialog:
        successDialog(folder)
    
    return folder