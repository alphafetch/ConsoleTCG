import util.scr as scr
import game as g
import util.key_vars as keyvars
import os

from colorama import init

# This contains important variables such as the user data directory
imp = keyvars.KeyVars()

# [*] This init() function is for colorama
init(autoreset=True)

while True:
    # Show the main menu
    u_input = scr.scr_main_menu()

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