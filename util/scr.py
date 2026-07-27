import os
import time

from . import sl
from . import help_func as helper
from . import key_vars as keyvars
from . import styles

# This contains important variables such as the user data directory
imp = keyvars.KeyVars()

# Main menu screen
def scr_main_menu() -> str:
    '''
    Defines & prints the main user interface using the colorama library.

    :return: Returns the user input after running through checks
    :rtype: str
    '''

    # Clear the screen
    helper.clear()

    # Print the menu
    print(styles.format_style("┌─────────────────────────┐", "bold_cyan"))
    print(styles.format_style("│ Welcome to Console TCG! │", "bold_cyan"))
    print(styles.format_style("└─────────────────────────┘\n", "bold_cyan"))
    print("1. Play Game")
    print("2. New Game (OVERWRITES)")
    print("3. View Collection")
    print("4. Quit")

    print()

    # Get user input and return it
    if os.path.exists(imp.user_data_toml):
        # [!] User has a save file
        u_input = helper.clean_input("> ", ["1", "2", "3", "4"])
    else:
        # [^] User does not have a save file
        u_input = helper.clean_input("> ", ["1", "2", "3", "4"], ["1", "3"], styles.format_style(f"Error: No user data. Please select a different option.", "error"))

    return u_input

def scr_collection() -> None:
    '''
    Show the collection screen.

    :rtype: None
    '''

    # [*] Clears the screen
    helper.clear()

    # 1. SET USER DATA PATH FOR QUICK ACCESS
    path = imp.user_data_toml

    # 2. ATTEMPT TO SHOW COLLECTIONS SCREEN
    try:
        # 3. LOAD THE USER DATA FROM THE USERDATA.TOML FILE
        data = sl.load(path)

        pass # [^] Stub
    except FileNotFoundError:
        # [;] Function failed, wait for the user to confirm
        print(styles.format_style("The save file could not be found and previous checks returned false.", "error"))
        input(styles.format_style("Press any key to continue...", "warn"))

        # [^] Return to the main menu
        return

def scr_tutorial() -> None:
    '''
    Show tutorial screen.

    :rtype: None
    '''

    print(styles.format_style("""
    │  Console TCG  │
    ├───────────────┤
    │   The first   │
    │  CLI trading  │
    │   card game!  │
    └───────────────┘
    
    """, "bold_cyan")) 

    print()

    print("How to play:")
    print("Roll cards for tokens!")
    print("Fight enemy cards!")
    print("Win tokens!")
    print("Repeat!")

    return