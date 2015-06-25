from src.tools.dialog import dialog

NAME_INPUT_HEADING = 'Give your new Collection a name:'


def successDialog(collection):    
    HEADING       =   'Congratulations!'
    LINE1         =   'Your new Collection [B]%s[/B] has been successfully created.'    %(collection.title)
    
    dialog.ok(HEADING, LINE1)