from colorama import Fore, Back, Style, init
from pathlib import Path

import util.sl_sys as sl
import util.help_func as helper
import util.key_vars as keyvars

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

    print(Fore.CYAN + Style.BRIGHT + "| Welcome to Console TCG! |")
    print(Fore.CYAN + Style.BRIGHT + "---------------------------")
    print()
    print("1. Play Game")
    print("2. View Collection")
    print("3. Quit")

    print()

    u_input = helper.clean_input("> ", ["1", "2", "3"])

    return u_input

def scr_collection() -> None:
    '''
    Show the collection screen.
    '''

    # Set user data file path for quick access
    path = imp.u_data_path

    data = sl.load(path)
    if data is None:
        raise FileNotFoundError("Save file missing or unreadable.")
    else:
        pass