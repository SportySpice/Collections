from src.tools.dialog import dialog

NAME_INPUT_HEADING = 'New folder name:'


INVALID_NAME_DIALOG = (
    "Error!",                   #heading
    "Invalid folder name."      #line1
)


FOLDER_EXISTS_DIALOG = (
    "Error!",                   #heading
    "Folder already exists."      #line1
)



def successDialog(folder):    
    HEADING       =   'Success!'
    LINE1         =   'Folder [B]%s[/B] has been successfully created.'    %(folder.name)
    
    dialog.ok(HEADING, LINE1)