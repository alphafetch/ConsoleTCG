from colorama import Fore, Back, Style, init

import util.sl_sys as sl_sys
import util.help_func as helper

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