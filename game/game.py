from util.help_func import quit

import util.sl as sl
import util.scr as scr
import util.key_vars as keyvars
import util.styles as styles
from . import tutorial

# This contains important variables such as the user data directory
imp = keyvars.KeyVars()

def new_game() -> None:
    '''
    Create a new game with a new user save file.

    :rtype: None
    '''

    # Create the data dictionary to save to the new file.
    data = {
        "user": {
            "items": [

            ],
            "weapons": [

            ],
            "armor": [

            ],
            "stats": {
                "health": 0,
                "new_game": 1,
                "xp": 0
            }
        },
    }

    # Save the dictionary to the user data TOML file for future use.
    sl.save(data, imp.user_data_toml)
    
    game()

def game() -> None:
    pass

def collection() -> None:
    '''
    Open the collection menu.

    :rtype: None
    '''

    scr.scr_collection()

def quit_cli() -> None:
    quit(0)