import util.sl_sys as sl_sys
import scr
import game as g

# Show the main menu
u_input = scr.scr_main_menu()

u_input = int(u_input)
match u_input:
    case 1:
        g.game()
    case 2:
        g.collection()
    case 3:
        g.quit_cli()
    case _: 
        raise ValueError("Value not accepted.")