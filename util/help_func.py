import sys
import subprocess
import random

from . import styles
from . import sl
from . import key_vars as keyvars

from typing import Any

from game.opponent import Opponent

# This contains important variables such as the user data directory
imp = keyvars.KeyVars()

def clean_input(prompt: str, requirements: list[str], disallowances: list[str] | None = None, disallow_message: str = "") -> str:
    '''
    Get output that (if the wrong input is entered) resets the line with a customizable error message.

    :param prompt: The prompt used for the input
    :type prompt: str

    :param requirements: What the user input must satisfy to continue
    :type requirements: list[str]

    :param disallowances: What the user input cannot be
    :type disallowances: list[str]

    :param disallow_message: What the output is if the user inputs a value that is disallowed
    :type disallow_message: str

    :return: Returns the correct user input, iterates until it returns this.
    :rtype: str
    '''

    # Check if there are no disallowances first 
    # and if it is, set it to an empty list
    if disallowances is None:
        disallowances = []

    error = ""
    has_error = False
    
    while True:
        # 1. Clear the error line from the previous iteration.
        # [*] \033[K clears from the cursor to the end of the line
        sys.stdout.write("\033[K" + error + "\r")
        
        # 2. If there was an error, move the cursor back to the input line
        # [*] \033[#A moves the cursor up # line(s)
        if has_error:
            sys.stdout.write("\033[2A")
        
        # 3. Clear the input line and replace with the prompt
        sys.stdout.write("\033[K" + prompt)
        # [*] Flush buffer
        sys.stdout.flush()
        
        # 4. Get input from the user
        u_input = sys.stdin.readline().strip()
        
        # 5. Validate the input
        # [*] Uses the requirements parameter to determine if the input
        # [*] can be accepted or not.
        if u_input in requirements:
            # [!] User input passes requirements, clear error slot
            if u_input in disallowances:
                # [^] Input was disallowed
                has_error = True
                error = str(styles.format_style(disallow_message, "error"))

                # Print a newline so the error message goes underneath the input
                sys.stdout.write("\n")
            else:
                # [!] Return user input - passed all tests
                sys.stdout.write("\n\033[K\033[1A\r")
                sys.stdout.flush()
                return u_input
        else:
            # [;] The loop failed to meet the requirements
            # [;] Set the error message for the next loop iteration
            has_error = True
            error = styles.format_style(f"Error: `{u_input}` is not a valid response. Please try again.", "error")
            
            # Print a newline so the error message goes underneath the input
            sys.stdout.write("\n")

def save_card(card: dict, cat: str) -> None:
    '''
    Saves a card to the userdata.toml file.

    :param card: A dictionary in the correct format for the card
    :type card: dict

    :param cat: The category to save to
    :type cat: str

    :rtype: None
    '''

    # [*] This function cannot be util.sl.modify_nested because
    # [*] this appends a dict to a list in a dictionary, instead
    # [*] of just modifying a key inside of a dictionary

    # 1. LOAD THE USER DATA
    user = sl.load(imp.user_data_toml)

    # 2. MODIFY IT TO ADD THE NEW CARD
    user["user"][cat.upper()].append(dict(card))

    # 3. SAVE THE USER DATA
    sl.save(user, imp.user_data_toml)


def print_card(card: dict, cat: str) -> None:
    '''
    Print a given card to the console.

    :param card: A dictionary in the correct format for the card
    :type card: dict

    :param cat: The category in which the card is in.
    :type cat: str

    :rtype: None
    '''

    cat = cat.upper()
    if cat != "ATK":
        eff = parse_effect_visual(card, cat)

    # This uses the inputted dictionary 
    # to show the card info to the user
    if cat == "ATK":
        print(styles.format_style(f"""┌───────────────┐
{card["name"]}
DMG: {card["damage"]}
MANA: {card["mana_cost"]}
TOK: {card["cost"]}
TYPE: {card["type"]}
└───────────────┘
DESC: {card["desc"]}""", "bold_cyan"))
    elif cat == "WPN":
        print(styles.format_style(f"""┌───────────────┐
{card["name"]}
MODIF: {eff}
MANA: {card["mana_cost"]}
TOK: {card["cost"]}
TYPE: {card["type"]}
└───────────────┘
DESC: {card["desc"]}""", "bold_cyan"))
    elif cat == "AMR":
        print(styles.format_style(f"""┌───────────────┐
{card["name"]}
MODIF: {eff}
MANA: {card["mana_cost"]}
TOK: {card["cost"]}
TYPE: {card["type"]}
└───────────────┘
DESC: {card["desc"]}""", "bold_cyan"))

# ----------------------------------------------------

def parse_effect_visual(card: dict, cat: str):
    if cat != "ATK":
        effects = parse_effect(card["effect"])
        final = []
        if effects: 
            for effect, value in effects.items():
                match effect:
                    case "damage_increase": final.append(f"Damage Increase: {value}")
                    case "poison": final.append(f"Poison: {value}")
                    case "skip_enemy_turn": final.append(f"Skip Enemy: {value}")
                    case "health_temp_increase": final.append(f"Health Increase: {value}")
                    case "defend_round": final.append(f"Defend Rounds: {value}")
        final_string = ', '.join(e for e in final)
        return final_string
    else:
        print("Failed execution of parse_effect_visual()")

def format_card_line(card_id: str, cards: dict[str, Any]) -> str:
    '''
    Formats a card into [####] [TYPE] Name format.

    :param card_id: The card ID to format.
    :type card_id: str,

    :param cards: The cards.
    :type cards: dict[str, Any]
    
    :return: The formatted string literal
    :rtype: str
    '''

    # Format the inputted card
    if card_id in cards["ATK"]:
        formatted_card = ""
        
        id_format = f"[{card_id[7:11]}] "
        formatted_card += id_format

        type_format = f"[{cards["ATK"][card_id]["type"].capitalize()}] "
        formatted_card += type_format

        name_format = f"{cards["ATK"][card_id]["name"]}"
        formatted_card += name_format

        formatted_card = styles.format_style(formatted_card, "red")
    elif card_id in cards["WPN"]:
        formatted_card = ""
                            
        id_format = f"[{card_id[7:11]}] "
        formatted_card += id_format

        type_format = f"[{cards["WPN"][card_id]["type"].capitalize()}] "
        formatted_card += type_format

        name_format = f"{cards["WPN"][card_id]["name"]}"
        formatted_card += name_format

        formatted_card = styles.format_style(formatted_card, "yellow")
    elif card_id in cards["AMR"]:
        formatted_card = ""
                            
        id_format = f"[{card_id[7:11]}] "
        formatted_card += id_format

        type_format = f"[{cards["AMR"][card_id]["type"].capitalize()}] "
        formatted_card += type_format

        name_format = f"{cards["AMR"][card_id]["name"]}"
        formatted_card += name_format

        formatted_card = styles.format_style(formatted_card, "cyan")
    else:
        formatted_card = "Empty Slot"
    return formatted_card

def get_category_from_index(i: int) -> str:
    '''
    Used for determining a card's category from where it is in a list.
    
    :param i: The index to check
    :type i: int

    :return: Returns the correct 3-letter abbreviated category
    :rtype: str
    '''
    
    return ( 
        "ATK" if i in range(0, 4) 
        else "WPN" if i in range(4, 6) 
        else "AMR" if i in range(6, 8)
        else "NAN"
    )

def get_category_from_id(id: str) -> str:
    '''
    Used for determining a card's category from its ID.

    :param id: The card id to check
    :type id: str

    :return: The category (3-letter abbreviated)
    :rtype: str
    '''

    cat = str(id[3] + id[4] + id[5])

    return cat.upper()

def reconstruct_id(four_digit: str, cat: str) -> str:
    '''
    Used to reconstruct a card ID from a four digit ID and a category.

    :param four_digit: The four digit ID to reconstruct from
    :type four_digit: str

    :param cat: The category
    :type cat: str

    :return: String card ID
    :rtype: str
    '''

    # Load the cards
    cards = sl.load(imp.cards_toml)

    for i in cards[cat.upper()]:
        if i[7:11] == four_digit:
            return str(i)
        else:
            continue

    return "" # Satisfy type checker

def create_randomized_opponent(diff: int) -> Opponent:
    '''
    Create a randomized opponent for exhibition mode.

    :param diff: The difficulty of the opponent
    :type diff: int

    :rtype: Opponent
    :return: An Opponent class initialization
    '''

    # 1. LOAD THE PROFILES TOML
    profiles = sl.load(imp.profiles_toml)

    # 2. CHOOSE A NAME
    name = random.choice(profiles["names"])

    # 3. SET HEALTH
    health = random.randint(
        profiles["health"][str(diff)]["min"], 
        profiles["health"][str(diff)]["max"],
    )

    # 4. SET DECK
    deck = []
    cards = sl.load(imp.cards_toml)
    cards_in_diff = []
    # Iterate through attack cards until one is found 
    # that is in the difficulty then add it to the 
    # cards_in_diff list
    for card in cards["ATK"]:
        if int(cards["ATK"][card]["diff"]) == diff:
            cards_in_diff.append(card)

    # Collect a sample of 4 from the cards in diff list
    # and add them to the deck
    rand_atk_cards = random.sample(list(cards_in_diff), 4)
    for card in rand_atk_cards:
        deck.append(card)

    # Do the same for weapons
    cards_in_diff = []
    for card in cards["WPN"]:
        if int(cards["WPN"][card]["diff"]) == diff:
            cards_in_diff.append(card)

    rand_wpn_cards = random.sample(list(cards_in_diff), 2)
    for card in rand_wpn_cards:
        deck.append(card)

    # Do the same for armor
    cards_in_diff = []
    for card in cards["AMR"]:
        if int(cards["AMR"][card]["diff"]) == diff:
            cards_in_diff.append(card)

    rand_amr_cards = random.sample(list(cards_in_diff), 2)
    for card in rand_amr_cards:
        deck.append(card)

    # 5. SET REWARD
    rew = random.choice(deck)

    # 6. SET THE TOKEN REWARD
    tok_rew = random.randint(
        profiles["token"][str(diff)]["min"], 
        profiles["token"][str(diff)]["max"],
    )

    # 7. SET THE XP REWARD
    xp = random.randint(
        profiles["xp"][str(diff)]["min"],
        profiles["xp"][str(diff)]["max"]
    )

    # 8. ELEMENTAL WEAK/RES
    elements = ["water", "fire", "sun", "nature", "earth"]
    match diff:
        case 1:
            weaksel = random.sample(elements, random.randint(2, 5))
            for weak in weaksel:
                elements.remove(weak)
            ressel = random.sample(elements, random.randint(0, len(elements) - 1 if len(elements) > 0 else len(elements)))
        case 2:
            weaksel = random.sample(elements, random.randint(1, 4))
            for weak in weaksel:
                elements.remove(weak)
            ressel = random.sample(elements, random.randint(0, len(elements) - 1))
        case 3:
            weaksel = random.sample(elements, random.randint(1, 3))
            for weak in weaksel:
                elements.remove(weak)
            ressel = random.sample(elements, random.randint(1, len(elements)))
        case 4:
            weaksel = random.sample(elements, random.randint(0, 2))
            for weak in weaksel:
                elements.remove(weak)
            ressel = random.sample(elements, random.randint(2, len(elements)))
        case 5:
            weaksel = random.sample(elements, random.randint(0, 1))
            for weak in weaksel:
                elements.remove(weak)
            ressel = random.sample(elements, random.randint(3, len(elements)))

    # 8. MATERIAL WEAK/RES
    materials = ["blade", "blunt", "hard", "wood"]
    match diff:
        case 1:
            weakmat = random.sample(materials, random.randint(2, 4))
            for weak in weakmat:
                materials.remove(weak)
            resmat = random.sample(materials, random.randint(0, len(materials) - 1 if len(materials) > 0 else len(materials)))
        case 2:
            weakmat = random.sample(materials, random.randint(1, 4))
            for weak in weakmat:
                materials.remove(weak)
            resmat = random.sample(materials, random.randint(0, len(materials) - 1 if len(materials) > 0 else len(materials)))
        case 3:
            weakmat = random.sample(materials, random.randint(1, 3))
            for weak in weakmat:
                materials.remove(weak)
            resmat = random.sample(materials, random.randint(1, len(materials)))
        case 4:
            weakmat = random.sample(materials, random.randint(0, 2))
            for weak in weakmat:
                materials.remove(weak)
            resmat = random.sample(materials, random.randint(2, len(materials)))
        case 5:
            weakmat = random.sample(materials, random.randint(0, 1))
            for weak in weakmat:
                materials.remove(weak)
            resmat = random.sample(materials, random.randint(3, len(materials)))

    # 10. CRIT CHANCE
    crit = random.randint(
        profiles["crit"][str(diff)]["min"],
        profiles["crit"][str(diff)]["max"]
    )

    # 11. SET UP THE OPPONENT
    opponent = Opponent(
        diff, name, health, 
        rew, deck, tok_rew,
        xp, 0, list(weaksel), list(ressel),
        list(weakmat), list(resmat), crit
    )

    # 12. RETURN THE OPPONENT
    return opponent

def parse_effect(effect_str: str) -> dict[str, int]:
    '''
    Parse an effect from cards.toml.

    :param effect_str: The effect to parse
    :type effect_str: str

    :return: The dictionary with the effects of the selected card
    :rtype: dict[str, int]
    '''

    effects = effect_str.split(",")

    parsed = {}
    for effect in effects:
        effect_pieces = effect.split("+")
        parsed[effect_pieces[0]] = int(effect_pieces[1])

    return parsed

def draw_random_card() -> dict[str, Any]:
    '''
    Draw a random card.

    :return: A dictionary with the card
    :rtype: dict[str, Any]
    '''

    cards = sl.load(imp.cards_toml)

    randomized = random.choices([1, 2, 3, 4, 5], weights=[59, 20, 10, 5, 1], k=1)[0]
    allowed_draw = {}

    randomized_cat = random.choice(["ATK", "WPN", "AMR"])

    for id, card in cards[randomized_cat].items():
        if card["diff"] == randomized:
            allowed_draw[id] = card

    ids = list(allowed_draw.keys())
    key = random.choice(ids)
    card = allowed_draw[key]
    return {"key": key, "value": card}

def clear() -> None: # REVIEW Spawns subprocess every time, may change
    '''
    Quickly and efficiently clears the screen

    :rtype: None
    '''

    subprocess.run("cls", shell=True)
    sys.stdout.write(styles.clear_styles())

def quit_game(code: str | int) -> None:
    '''
    Exits with exit code 0

    :param code: The exit code for the program
    :type code: str | int

    :rtype: None
    '''

    sys.exit(code)
