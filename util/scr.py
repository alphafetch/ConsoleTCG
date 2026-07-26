from colorama import Fore, Back, Style, init
from pathlib import Path
import os

import util.sl_sys as sl
import util.help_func as helper
import util.key_vars as keyvars
import util.styles as styles

# INFO: Important variable storage (such as user data directories and files)
imp = keyvars.KeyVars()

# Main menu screen
def scr_main_menu() -> str:
    '''
    Defines & prints the main user interface using the colorama library.

    :return: Returns the user input after running through checks
    :rtype: str
    '''

    init(autoreset=True)

    print(styles.format_style("| Welcome to Console TCG! |", "bold_cyan"))
    print(styles.format_style("---------------------------", "bold_cyan"))
    print()
    print("1. Play Game")
    print("2. New Game (OVERWRITES)")
    print("3. View Collection")
    print("4. Quit")

    print()

    if os.path.exists(imp.user_data_toml):
        u_input = helper.clean_input("> ", ["1", "2", "3", "4"], [])
    else:
        u_input = helper.clean_input("> ", ["1", "2", "3", "4"], ["1", "3"])

    return u_input

def scr_collection() -> None:
    '''
    Show the collection screen.
    '''

    # Set user data file path for quick access
    path = imp.user_data_toml

    data = sl.load(path)
    if data is None:
        raise FileNotFoundError("Save file missing or unreadable.")
    else:
        pass