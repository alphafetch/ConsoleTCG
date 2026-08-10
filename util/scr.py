import os
import time

from . import sl
from . import help_func as helper
from . import key_vars as keyvars
from . import styles

from game import exhibition as exhib

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

    :return: Returns a bool signaling if game() should continue or not
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
2. Exhibition
3. Decks (TBA)
4. Main Menu\n""")

    u_input = helper.clean_input("> ", ["1", "2", "3", "4"], ["1", "3"], styles.format_style("Error: That option is not ready yet.", "error"))

    match int(u_input):
        case 2:
            # Start the exhibition script
            exhib.start_exhibition()

            return False
        case 4:
            return True
        case _:
            return False

def scr_diff_select_exhibition() -> int:
    '''
    Screen to select a difficulty for an exhibition game.

    :return: Returns the difficulty level as an integer (easy: 1, medium: 2, hard: 3)
    :rtype: int
    '''

    # Clear the screen
    helper.clear()

    print(styles.format_style("""SELECT DIFFICULTY:
1. Easy
2. Normal
3. Medium
4. Hard
5. Extreme\n""", "cyan_back"))

    diff = helper.clean_input("> ", ["1", "2", "3", "4", "5"])

    return int(diff)

def scr_decks() -> None:
    '''
    Customize decks. Empty slots (in a new OR old file) are represented by "empty".

    :rtype: None
    '''

    # Clear the screen
    helper.clear()

    # Deck Selection
    if not os.path.exists(imp.user_decks_toml):
        decks = {
            "decks": {
                "deck1": {
                    "cards": [
                        "empty", "empty", "empty", "empty", 
                        "empty", "empty", "empty", "empty"
                    ]
                },
                "deck2": {
                    "cards": [
                        "empty", "empty", "empty", "empty", 
                        "empty", "empty", "empty", "empty"
                    ]
                },
                "deck3": {
                    "cards": [
                        "empty", "empty", "empty", "empty", 
                        "empty", "empty", "empty", "empty"
                    ]
                }
            }
        }

        sl.save(decks, imp.user_decks_toml)

    decks = sl.load(imp.user_decks_toml)

    # Check if decks are empty or not
    deck1_empty = None
    deck2_empty = None
    deck3_empty = None

    for id in decks["decks"]["deck1"]["cards"]:
        if id == "empty":
            continue
        else:
            deck1_empty = "In Use"
            break

    for id in decks["decks"]["deck2"]["cards"]:
            if id == "empty":
                continue
            else:
                deck2_empty = "In Use"
                break

    for id in decks["decks"]["deck3"]["cards"]:
            if id == "empty":
                continue
            else:
                deck3_empty = "In Use"
                break

    # Set the decks to empty if they haven't already been in use
    if deck1_empty is None: deck1_empty = "Empty"
    if deck2_empty is None: deck2_empty = "Empty"
    if deck3_empty is None: deck3_empty = "Empty"

    # Print decks (empty or in use)
    print(styles.format_style(f"Deck 1: {deck1_empty}", "cyan"))
    print(styles.format_style(f"Deck 2: {deck2_empty}", "cyan"))
    print(styles.format_style(f"Deck 3: {deck3_empty}\n", "cyan"))

    # Ask which deck to edit
    deck = helper.clean_input("Deck # to Edit (Q to quit): ", ["1", "2", "3", "Q", "q"])

    # If the user wants to quit, return
    if deck == "Q" or deck == "q":
        # [^] Return to the menu
        return

    # Move to deck-specific menu
    scr_show_deck(int(deck))

def scr_show_deck(deck_num: int) -> None:
    '''
    Show the specified deck.

    :param deck_num: The deck number to show
    :type deck_num: int

    :rtype: None
    '''

    while True:
        # Clear the screen
        helper.clear()

        # Load the deck
        decks = sl.load(imp.user_decks_toml)
        cards = sl.load(imp.cards_toml)

        # Load each card in deck to a list
        for i, card in enumerate(decks["decks"]["deck" + str(deck_num)]["cards"]):
            if card == "empty":
                # Prints: #. Empty [CAT]
                print(f"{i + 1}. Empty [{helper.get_category_from_index(i)}]")
            else:
                # Prints: #. [NAME] [CAT]
                correct_color = (
                    "red" if helper.get_category_from_index(i) == "ATK"
                    else "yellow" if helper.get_category_from_index(i) == "WPN"
                    else "cyan" if helper.get_category_from_index(i) == "AMR"
                    else "cyan"
                )
                
                print(
                    styles.format_style(
                        f"{i + 1}. {cards[helper.get_category_from_index(i)][card]["name"]} [{helper.get_category_from_index(i)}]",
                        correct_color,
                    ),
                )

        print()

        # See what card the user wants to edit (or quit)
        u_input = helper.clean_input(
            "Select card to edit (Q to quit): ", 
            ["1", "2", "3", "4", "5", "6", "7", "8", "Q", "q"],
        )

        if u_input.upper() == "Q":
            break
        else:
            scr_show_card_in_deck(int(u_input) - 1, deck_num)

    return

def scr_show_card_in_deck(card: int, deck: int) -> None:
    '''
    Shows a card in a deck.

    :param card: The card # to edit - 0-based
    :type card: int

    :param deck: The deck in which the card is - 1-based
    :type deck: int

    :rtype: None
    '''

    # Clear the screen
    helper.clear()

    # Load user decks
    decks = sl.load(imp.user_decks_toml)
    cards = sl.load(imp.cards_toml)
    card_id = decks["decks"]["deck" + str(deck)]["cards"][card]

    # Check if the card is empty or not
    if not card_id == "empty":
        # Get card category
        category = helper.get_category_from_id(card_id)
        # Print the card and ask if the user wants to select a new one or quit
        helper.print_card(cards[category][card_id], category)
        u_input = helper.clean_input("\nEdit card? (Y/n): ", ["Y", "N", "y", "n"])
        if u_input.upper() == "N":
            return
        else: scr_edit_card_in_deck(card_id, "deck" + str(deck), card) # Edit the card
    else:
        scr_edit_card_in_deck(card_id, "deck" + str(deck), card)

def scr_edit_card_in_deck(card_id: str, deck: str, index: int) -> None:
    '''
    Edits a card in a deck.
    
    :param card_id: The card ID to edit
    :type card_id: str

    :param deck: The deck in which the card is - 1-based
    :type deck: str

    :param index: The card index to edit - 0-based
    :type index: int

    :rtype: None
    '''

    # Clear the screen
    helper.clear()

    # 1. GET THE CARD'S CATEGORY
    cat = helper.get_category_from_index(index)

    # 2. GET THE PLAYER'S CARDS & DECKS
    player_cards = sl.load(imp.user_data_toml)["user"][cat]
    player_decks = sl.load(imp.user_decks_toml)

    cards = sl.load(imp.cards_toml)

    # 3. TALLY UP DUPLICATES
    tally = {}
    for card in player_cards:
        if card["id"] in tally:
            tally[card["id"]] += 1
        elif not card["id"] in tally:
            tally[card["id"]] = 1

    # 4. TALLY UP USED CARDS
    used_tally = {}
    for card in player_decks["decks"][deck]["cards"]:
        if card in used_tally and card != "empty":
            used_tally[card] += 1
        elif not card in used_tally and card != "empty":
            used_tally[card] = 1

    # 5. FILTER FOR SELECTION
    for card in used_tally:
        tally[card] -= used_tally[card]
    for card in list(tally.keys()):
        if tally[card] <= 0:
            tally.pop(card)

    # 6. CHECK IF FILTER IS EMPTY
    if not tally:
        print(styles.format_style("No cards available. Press any key to continue...", "warn"))
        input()
        return

    # 7. FORMAT THE CARDS AND ADD THEM TO A LIST
    formatted_cards_list = []
    for id in tally:
        formatted_card = helper.format_card_line(id, cards)

        formatted_cards_list.append(formatted_card)

    # 8. OUTPUT THE CARDS
    print(styles.format_style("Enter the ID at the bottom (first value on each line) to select a card.", "bold_cyan"))
    print(styles.format_style("These are your available cards:", "cyan"))

    for formatted in formatted_cards_list:
        print(formatted)

    # Make the list of 4 digit ID numbers for clean_input()
    four_digit_ids = []
    for i in tally:
        four_digit_ids.append(i[7:11])

    four_uid = helper.clean_input("ID: ", four_digit_ids)

    # 9. ADD THE CARD TO THE USERDECKS.TOML FILE
    # Reconstruct the ID
    uid = helper.reconstruct_id(four_uid, cat)

    # Update the decks file
    sl.modify_nested(["decks", deck, "cards", index], uid, imp.user_decks_toml)

    # 10. SHOW A SAVED CARD SCREEN
    # Clear the screen
    helper.clear()

    print(styles.format_style("Card saved!", "progress"))
    time.sleep(1)
    return