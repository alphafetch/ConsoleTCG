from colorama import init

import util.scr as scr
import util.key_vars as keyvars

import game.menu_logic as g

# This contains important variables such as the user data directory
imp = keyvars.KeyVars()

# [*] This init() function is for colorama
init(autoreset=True)

while True:
    # Show the main menu
    u_input = scr.scr_main_menu()

    # Match/case statement to determine correct course of action
    # for the user's input
    u_input = int(u_input)
    match u_input:
        case 1:
            g.game()
        case 2:
            g.new_game()
        case 3:
            g.collection()
        case 4:
            g.quit_cli()