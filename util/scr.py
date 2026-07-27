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

    print(styles.format_style("""┌───────────────┐
│  Console TCG  │
├───────────────┤
│   The first   │
│  CLI trading  │
│   card game!  │
└───────────────┘""", "bold_cyan")) 

    print("How to play:")
    print("Roll cards for tokens!")
    print("Fight enemy cards!")
    print("Win tokens!")
    print("Repeat!")

    return

def scr_starter_card() -> None:
    '''
    A small menu to choose the player's starting card.

    :rtype: None
    '''

    # Clear the screen
    helper.clear()

    # 1. LOAD THE CARDS TOML FILE
    cards = sl.load(imp.cards_toml)

    # 2. CREATE AN EMPTY STARTER DECK LIST
    starters = []

    # 3. ITERATE THROUGH ATTACK CARDS, IF IT IS A STARTER
    #    APPEND THE CARD TO THE LIST
    for id, card in cards["atk"].items():
        if card["starter"] == True:
            card["id"] = id
            starters.append(card)
        else: continue

    # 4. FOR EVERY STARTER CARD, PRINT IT AND ASK THE USER
    #    TO TAKE IT OR LEAVE IT
    for card in starters:
        helper.clear()
        helper.print_card(card)
        print()
        input(styles.format_style("Press any key to continue to the next card...", "warn"))
        continue

    helper.clear()

    # 5. ASK THE USER TO CHOOSE THE CARD THEY WANT
    card = helper.clean_input("Which card would you like to choose? (1-5): ", ["1", "2", "3", "4", "5"])

    # 6. SAVE THE CARD TO THE USER'S DATA FILE
    helper.clear() 
    print(styles.format_style("Saving card...", "progress"))

    # [*] This function is a helper function to save
    # [*] any and all cards to the userdata.toml file
    helper.save_card(starters[int(card) - 1])

    # Sleep so the user sees the "Saving card..." line
    time.sleep(0.5)

    return

def scr_status() -> bool:
    '''
    The status menu for the main game.

    :rtype: bool
    '''

    # Clear the screen
    helper.clear()

    # Load the user data
    data = sl.load(imp.user_data_toml)

    # Print the stat menu
    print(styles.format_style(f"""┌───────────────┐
│ Statistics:
│ Wins: {data["user"]["stats"]["wins"]}
│ Losses: {data["user"]["stats"]["losses"]}
│ XP: {data["user"]["stats"]["xp"]}
│ Max HP: {data["user"]["stats"]["max_hp"]}
└───────────────┘\n""", "bold_cyan"))
    print("""1. Career (TBA)
2. Exhibition (WIP)
3. Decks (TBA)
4. Main Menu\n""")

    u_input = helper.clean_input("> ", ["1", "2", "3", "4"], ["1", "2", "3"], styles.format_style("Error: That option is not ready yet.", "error"))

    match int(u_input):
        case 4:
            return True
        case _:
            return False