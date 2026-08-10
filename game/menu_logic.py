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
            "ATK": [

            ],
            "WPN": [

            ],
            "AMR": [

            ],
            "stats": {
                "new_game": 1,
                "xp": 0,
                "wins": 0,
                "losses": 0,
                "max_hp": 100
            }
        },
    }

    # Save the dictionary to the user data TOML file for future use.
    sl.save(data, imp.user_data_toml)
    
    game()

def game() -> None:
    '''
    Runs the main game.

    :rtype: None
    '''

    while True:
        # 1. LOAD THE USER DATA FROM THE USERDATA.TOML FILE
        try:
            data = sl.load(imp.user_data_toml)
        except FileNotFoundError:
            # [;] Function failed, wait for the user to confirm
            print(styles.format_style("The save file could not be found and previous checks returned false.", "error"))
            input(styles.format_style("Press any key to continue...", "warn"))

            # [^] Return to the main menu
            return

        # 2. CHECK IF THE USER IS A NEW PLAYER
        if data["user"]["stats"]["new_game"] == 1:
            # [!] User is a new player, run the tutorial
            t_success = tutorial.run()

            if t_success:
                # 3. IF THE TUTORIAL WAS SUCCESSFUL, RETURN TO THE MENU
                return
            else:
                # [;] Function failed, wait for the user to confirm
                print(styles.format_style("The data edit did not succeed.", "error"))
                input(styles.format_style("Press any key to continue...", "warn"))

                # [^] Return to the main menu
                return
        else:
            # Move to the status menu
            ret = scr.scr_status()
            if ret:
                return
            else:
                continue
        
def collection() -> None:
    '''
    Open the collection menu.

    :rtype: None
    '''

    scr.scr_collection()

def quit_cli() -> None:
    quit(0)