import os
import time
import readchar
import random

from . import sl
from . import help_func as helper
from . import key_vars as keyvars
from . import styles

from game import exhibition as exhib
from game import match as matchmaker
from game import opponent as opp

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

def scr_collection() -> None: # TODO Collections
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
        print(styles.format_style("Press any key to continue...", "warn"))
        readchar.readkey()

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
    for id, card in cards["ATK"].items():
        if card["starter"] == True:
            card["id"] = id
            starters.append(card)
        else: continue

    # 4. FOR EVERY STARTER CARD, PRINT IT AND ASK THE USER
    #    TO TAKE IT OR LEAVE IT
    for card in starters:
        helper.clear()
        helper.print_card(card, "ATK")
        print()
        print(styles.format_style("Press any key to continue to the next card...", "warn"))
        readchar.readkey()
        continue

    helper.clear()

    # 5. ASK THE USER TO CHOOSE THE CARD THEY WANT
    card = helper.clean_input("Which card would you like to choose? (1-5): ", ["1", "2", "3", "4", "5"]) # REVIEW Cannot have more or less starters, may change

    # 6. SAVE THE CARD TO THE USER'S DATA FILE
    helper.clear() 
    print(styles.format_style("Saving card...", "progress"))

    # [*] This function is a helper function to save
    # [*] any and all cards to the userdata.toml file
    helper.save_card(starters[int(card) - 1], "ATK")

    # Sleep so the user sees the "Saving card..." line
    time.sleep(2)

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
│ Crit %: {data["user"]["stats"]["crit"]}
│ Level: {data["user"]["stats"]["lvl"]}
│ Tokens: {data["user"]["stats"]["tokens"]}
└───────────────┘\n""", "bold_cyan"))
    print("""1. Career
2. Exhibition
3. Decks
4. Roll Card (TBA)
5. Main Menu\n""")

    # Get the user's input on what they would like to do
    u_input = helper.clean_input("> ", ["1", "2", "3", "4", "5"], ["4"], styles.format_style("Error: That option is not ready yet.", "error")) 

    u_input = int(u_input)
    if not u_input in [1, 2, 3, 4, 5]:
        raise ValueError("User input did not pass clean_input() and is not a correct value.")

    match u_input:
        case 1:
            scr_career()

            return False
        case 2:
            # Start the exhibition script
            exhib.start_exhibition()

            return False
        case 3: 
            scr_decks()

            return False
        case 4:
            return False
        case 5:
            return True
    # Fallback return to satisfy error messages - unreachable
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

def scr_career() -> bool | None:
    '''
    The main career menu with worlds.

    :return: The execution success
    :rtype: bool | None
    '''

    # Clear the screen
    helper.clear()

    # 1. FLOODGATES FOR NEW PLAYERS
    if not os.path.exists(imp.user_data_toml): # User data missing
        # [;] User data file is missing
        print(styles.format_style("You have not set up your data. Please visit the new game menu.", "error"))
        print(styles.format_style("Press any key to return...", "warn"))
        readchar.readkey()
        return
    elif not os.path.exists(imp.user_decks_toml): # User deck file is missing
        # [;] User deck file is missing
        print(styles.format_style("You have not set up your decks. Please visit the decks menu.", "error"))
        print(styles.format_style("Press any key to return...", "warn"))
        readchar.readkey()
        return

    # 1a. LOAD RELEVANT FILES
    userdata = sl.load(imp.user_data_toml)
    userdecks = sl.load(imp.user_decks_toml)

    if userdata["unlocks"]["career"]["unlocked"] == False: # Check if career is unlocked yet
        # [;] User has not unlocked career yet
        print(styles.format_style("You have not unlocked career mode yet.", "error"))
        print(styles.format_style("Press any key to return...", "warn"))
        readchar.readkey()
        return
    elif len(userdata["user"]["ATK"]) == 0: # Even if user has WPN or AMR cards, they can't deal damage w/o ATK cards
        # [;] User does not have enough cards
        print(styles.format_style("You do not have enough ATK cards to continue (req: 1).", "error"))
        print(styles.format_style("Press any key to return...", "warn"))
        readchar.readkey()
        return

    deck1_empty = True
    for i in userdecks["decks"]["deck1"]["cards"]:
        if i != "empty": deck1_empty = False; break
        else: continue
    deck2_empty = True
    for i in userdecks["decks"]["deck2"]["cards"]:
        if i != "empty": deck2_empty = False; break
        else: continue
    deck3_empty = True
    for i in userdecks["decks"]["deck3"]["cards"]:
        if i != "empty": deck3_empty = False; break
        else: continue

    if deck1_empty and deck2_empty and deck3_empty: # The user hasn't set any decks even after visiting the menu
        # [;] User has not set any decks
        print(styles.format_style("You have not set any decks. Please visit the decks menu.", "error"))
        print(styles.format_style("Press any key to return...", "warn"))
        readchar.readkey()
        return

    return scr_world_select()

def scr_win_career(world: int, opponent: opp.Opponent, num: int) -> None:
    '''
    Win screen after a battle.

    :param world: The world the player just beat an enemy in
    :type world: int

    :param opponent: The opponent object
    :type opponent: Opponent

    :param num: The enemy number
    :type num: int

    :rtype: None
    '''

    # 1. LOAD RELEVANT FILES
    data = sl.load(imp.user_data_toml)
    cards = sl.load(imp.cards_toml)
    career = sl.load(imp.career_toml)
    levels = sl.load(imp.lvls_toml)

    # Clear the screen
    helper.clear()

    # 2. GIVE CARD REWARD
    # Determine whether this is the first time fighting
    if data["unlocks"]["career"]["progress"]["world" + str(world)][str(num)] == True:
        new_win = False
        card_data = helper.draw_random_card(opponent.diff)
        id = card_data["key"]
        card = card_data["value"]
        cat = id[3:6].upper()
    else:
        new_win = True
        cat = career["world" + str(world)][str(num)]["reward"][3:6].upper()
        card = cards[cat][career["world" + str(world)][str(num)]["reward"]]
        id = career["world" + str(world)][str(num)]["reward"]

    # 3. SAVE THE CARD & SET WIN IF NEW WIN
    card["id"] = id
    helper.save_card(card, cat)
    if new_win: sl.modify_nested(["unlocks", "career", "progress", "world" + str(world), str(num)], True, imp.user_data_toml)

    # 4. PAYOUT
    # Tokens
    plus_toks = opponent.tokens
    new_toks = data["user"]["stats"]["tokens"] + plus_toks
    sl.modify_nested(["user", "stats", "tokens"], new_toks, imp.user_data_toml)
    # XP
    plus_xp = round(opponent.xp * random.uniform(0.8, 1.2))
    new_xp = data["user"]["stats"]["xp"] + plus_xp
    sl.modify_nested(["user", "stats", "xp"], new_xp, imp.user_data_toml)

    # 5. INCREMENT WINS
    new_wins = data["user"]["stats"]["wins"] + 1
    sl.modify_nested(["user", "stats", "wins"], new_wins, imp.user_data_toml)

    # 6. CHECK FOR A WORLD UNLOCK
    complete = True
    for k, v in data["unlocks"]["career"]["progress"]["world" + str(world)].items():
        if k == "unlocked": continue
        if v == True:
            complete = True
            continue
        else:
            complete = False
            break

    if complete:
        data["unlocks"]["career"]["progress"]["world" + str(world + 1)]["unlocked"] = True
        sl.save(data, imp.user_data_toml)

    # 7. PRINT
    print(styles.format_style("You won!", "success"))
    print("------------------")
    print(styles.format_style("Reward:", "bold_cyan"))
    helper.print_card(card, cat)
    print("------------------")
    print(f"Tokens: {styles.format_style("+" + str(plus_toks), "green")} - TOTAL: {styles.format_style(str(new_toks), "green")}")
    print(f"XP: {styles.format_style("+" + str(plus_xp), "progress")} - TOTAL: {styles.format_style(str(new_xp), "progress")}")
    print(f"+1 Win - TOTAL: {styles.format_style(str(new_wins), "yellow")}")
    if complete: print(f"Unlocked {styles.format_style("World " + str(world + 1), "cyan")}!")
    print("Press any key to continue...")
    readchar.readkey()

    data = sl.load(imp.user_data_toml)

    # 8. CHECK FOR LEVEL UP
    if data["user"]["stats"]["lvl"] + 1 <= levels["max"]["max_lvl"]:
        if data["user"]["stats"]["xp"] >= levels[str(data["user"]["stats"]["lvl"] + 1)]["thresh"]:
            sl.modify_nested(["user", "stats", "lvl"], data["user"]["stats"]["lvl"] + 1, imp.user_data_toml); data = sl.load(imp.user_data_toml)
            sl.modify_nested(["user", "stats", "crit"], levels[str(data["user"]["stats"]["lvl"])]["crit"], imp.user_data_toml); data = sl.load(imp.user_data_toml)
            sl.modify_nested(["user", "stats", "tokens"], data["user"]["stats"]["tokens"] + levels[str(data["user"]["stats"]["lvl"])]["toks"], imp.user_data_toml); data = sl.load(imp.user_data_toml)
            sl.modify_nested(["user", "stats", "max_hp"], levels[str(data["user"]["stats"]["lvl"])]["hp"], imp.user_data_toml); data = sl.load(imp.user_data_toml)

            # 9. PRINT LEVEL UP
            helper.clear()
            print(styles.format_style("LEVEL UP", "success"))
            print("New Level: " + styles.format_style(str(data["user"]["stats"]["lvl"]), 
                                                    "progress" if data["user"]["stats"]["lvl"] < 4 \
                                                    else "cyan" if data["user"]["stats"]["lvl"] < 8 \
                                                    else "green"
                                                    ))
            print(f"+ {styles.format_style(str(levels[str(data["user"]["stats"]["lvl"])]["toks"]) + " Tokens", "yellow")}")
            print(f"Crit %: {levels[str(data["user"]["stats"]["lvl"])]["crit"]}%")
            print(f"New Max HP: {styles.format_style(str(levels[str(data["user"]["stats"]["lvl"])]["hp"]), "green")}")
            print("Press any key to continue...")
            readchar.readkey()

    return

def scr_lose_career():
    pass

def scr_world_select() -> None | bool:
    '''
    Select a world to enter.

    :return: The player's win status
    :rtype: None | bool
    '''

    # Clear the screen
    helper.clear()

    # Load relevant files
    user = sl.load(imp.user_data_toml)

    # Print worlds
    disallowed_list = []
    for i in range(7):
        if user["unlocks"]["career"]["progress"]["world" + str(i + 1)]["unlocked"] == True:
            print(styles.format_style("World " + str(i + 1), "cyan"))
        else:
            print(styles.format_style("World " + str(i + 1), "red"))
            disallowed_list.append(str(i + 1))
    print()

    world = helper.clean_input("Select world (Q/q to quit): ", ["1", "2", "3", "4", "5", "6", "7", "Q", "q"], disallowed_list, "That world is not unlocked yet!")

    if world == "Q" or world == "q":
        return

    return scr_enemy_select(int(world))

def scr_enemy_select(world: int) -> None | bool:
    '''
    Select an enemy to battle.

    :return: Player win status
    :rtype: None | bool
    '''

    # Clear the screen
    helper.clear()

    # Load relevant files
    user = sl.load(imp.user_data_toml)
    career = sl.load(imp.career_toml)

    # Print enemies
    disallowed_list = []
    allowed_list = []
    # [*]           V this gets # of enemies in world
    for index in range(1, len(career["world" + str(world)]) + 1):
        if index == 1: 
            allowed_list.append(career["world" + str(world)][str(index)])
            continue
        elif user["unlocks"]["career"]["progress"]["world" + str(world)][str(index)] == True:
            allowed_list.append(career["world" + str(world)][str(index)])
            continue
        elif user["unlocks"]["career"]["progress"]["world" + str(world)][str(index)] == False\
            and user["unlocks"]["career"]["progress"]["world" + str(world)][str(index - 1)]: 
                allowed_list.append(career["world" + str(world)][str(index)])
                continue
        else: 
            disallowed_list.append(str(index))

    for i, enemy in enumerate(allowed_list):
        formatted_enemy = ""

        formatted_enemy += f"{i + 1}. "

        stars = ""
        for i in range(enemy["diff"]):
            stars += "★"
        for i in range(5 - len(stars)):
            stars += "☆"

        formatted_enemy += f"[{stars}] "
        formatted_enemy += enemy["name"]

        match enemy["diff"]:
            case 1: formatted_enemy = styles.format_style(formatted_enemy, "green")
            case 2: formatted_enemy = styles.format_style(formatted_enemy, "cyan")
            case 3: formatted_enemy = styles.format_style(formatted_enemy, "yellow")
            case 4: formatted_enemy = styles.format_style(formatted_enemy, "progress")
            case 5: formatted_enemy = styles.format_style(formatted_enemy, "red")

        print(formatted_enemy)

    print()

    enemy = helper.clean_input("Select enemy: ", [(str(x + 1)) for x in range(len(career["world" + str(world)]))], disallowed_list, "Defeat the previous enemy first!")

    opponent = allowed_list[int(enemy) - 1]
    opponent_ = opp.Opponent(
        opponent["diff"], opponent["name"],
        opponent["health"], opponent["reward"],
        opponent["deck"], opponent["tokens"],
        opponent["xp"], opponent["id"],
        opponent["weak-el"], opponent["res-el"],
        opponent["weak-mat"], opponent["res-mat"],
        opponent["crit"]
    )

    return scr_show_enemy(world, opponent_, int(enemy))

def scr_show_enemy(world: int, opponent: opp.Opponent, enemy: int) -> None | bool:
    '''
    Shows an enemy's stats before a battle.

    :param world: The world that the user is in
    :type world: int

    :param opponent: The enemy to display
    :type opponent: Opponent

    :param enemy: The enemy's number in the world
    :type enemy: int

    :return: If the player won or not
    :rtype: None | bool
    '''

    # Clear the screen
    helper.clear()

    # Load relevant files
    cards = sl.load(imp.cards_toml)

    # Show enemy statistics
    # 1. Main stats
    print(styles.format_style(f"{opponent.name} | STATS:", "bold_cyan"))
    print(styles.format_style(f"HP: {opponent.health}", "cyan"))
    print(styles.format_style(f"CRIT %: {str(opponent.crit)}%", "cyan"))
    print(styles.format_style(f"TOK: {str(opponent.tokens)}", "cyan"))
    print(styles.format_style(f"REW: {helper.format_card_line(opponent.reward, cards)}", "cyan"))

    # 2. Difficulty level
    stars = ""
    for _ in range(opponent.diff):
        stars += "★"
    for _ in range(5 - len(stars)):
        stars += "☆"
    match opponent.diff:
        case 1: stars = styles.format_style(stars, "green")
        case 2: stars = styles.format_style(stars, "cyan")
        case 3: stars = styles.format_style(stars, "yellow")
        case 4: stars = styles.format_style(stars, "progress")
        case 5: stars = styles.format_style(stars, "red")
    print(f"DIFF: {stars}")

    print("----------------------")

    # 3. Deck
    print(styles.format_style("DECK:", "red"))
    for card in opponent.deck:
        print(helper.format_card_line(card, cards))

    print("----------------------")

    # 4. Resistances and weaknesses
    print(styles.format_style("WEAKNESSES:", "green"))
    if opponent.weak_el or opponent.weak_mat:
        for weakness in opponent.weak_el + opponent.weak_mat:
            weakness_formatted = weakness.capitalize()
            match weakness_formatted:
                case "Fire": weakness_formatted = styles.format_style(weakness_formatted, "red")
                case "Water": weakness_formatted = styles.format_style(weakness_formatted, "cyan")
                case "Earth": weakness_formatted = styles.format_style(weakness_formatted, "green")
                case "Nature": weakness_formatted = weakness_formatted
                case "Sun": weakness_formatted = styles.format_style(weakness_formatted, "error")
                case "Blade": weakness_formatted = weakness_formatted
                case "Blunt": weakness_formatted = styles.format_style(weakness_formatted, "red")
                case "Hard": weakness_formatted = styles.format_style(weakness_formatted, "cyan")
                case "Wood":  weakness_formatted = styles.format_style(weakness_formatted, "progress")
            print(weakness_formatted)
    else:
        print(styles.format_style("No elemental/material weaknesses.", "red"))
    print("----------------------")
    print(styles.format_style("RESISTANCES:", "red"))
    if opponent.res_el or opponent.res_mat:
        for res in opponent.res_el + opponent.res_mat:
            res_formatted = res.capitalize()
            match res_formatted:
                case "Fire": res_formatted = styles.format_style(res_formatted, "red")
                case "Water": res_formatted = styles.format_style(res_formatted, "cyan")
                case "Earth": res_formatted = styles.format_style(res_formatted, "green")
                case "Nature": res_formatted = res_formatted
                case "Sun": res_formatted = styles.format_style(res_formatted, "error")
                case "Blade": res_formatted = res_formatted
                case "Blunt": res_formatted = styles.format_style(res_formatted, "red")
                case "Hard": res_formatted = styles.format_style(res_formatted, "cyan")
                case "Wood":  res_formatted = styles.format_style(res_formatted, "progress")
            print(res_formatted)
    else:
        print(styles.format_style("No elemental/material resistances.", "green"))

    # Ask if the user wants to fight the opponent
    print()
    u_input = helper.clean_input("Would you like to fight this opponent? (Y/n): ", ["y", "n", "Y", "N"])
    if u_input.lower() == "y":
        win = matchmaker.start_match(world, opponent, enemy)
        if win: scr_win_career(world, opponent, enemy)
        else: scr_lose_career()
        return win
    else: return

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
        u_input = helper.clean_input("\nEdit card? (Y/n, D/d to delete): ", ["Y", "N", "D", "d", "y", "n"])
        if u_input.upper() == "N":
            return
        elif u_input.upper() == "D":
            scr_delete_card_in_deck(card, "deck" + str(deck))
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
        if card == "empty":
            continue
        if helper.get_category_from_id(card) != cat:
            continue
        if card in used_tally:
            used_tally[card] += 1
        else:
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
        readchar.readkey()
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
    time.sleep(2)
    return

def scr_delete_card_in_deck(card: int, deck: str) -> None:
    '''
    Deletes a card in a deck.

    :param card: The card index to remove
    :type card: int

    :param deck: The deck to remove it from
    :type deck: str

    :rtype: None
    '''

    # Clear the screen
    helper.clear()

    # Find the correct card in the decks file and remove it
    sl.modify_nested(["decks", deck, "cards", card], "empty", imp.user_decks_toml)

    # Give output to the user
    print(styles.format_style("Card removed from deck!", "progress"))
    time.sleep(2)
    return