import sys
import subprocess
import random

from . import styles
from . import sl
from . import key_vars as keyvars

from game.opponent import Opponent

# This contains important variables such as the user data directory
imp = keyvars.KeyVars()

def clean_input(prompt: str, requirements: list[str], disallowances: list[str] | None = None, disallow_message: str = "") -> str:
    '''
    Get output that (if the wrong input is entered) resets the line with a customizable error message.

    :param prompt: The prompt used for the input
    :param requirements: What the user input must satisfy to continue
    :param disallowances: What the user input cannot be
    :param disallow_message: What the output is if the user inputs a value that is disallowed

    :type prompt: str
    :type requirements: list[str]
    :type disallowances: list[str]
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
                error = str(disallow_message)

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

def save_card(card: dict) -> None:
    '''
    Saves a card to the userdata.toml file.

    :param card: A dictionary in the correct format for the card
    :type card: dict

    :rtype: None
    '''

    # [*] This function cannot be util.sl.modify_nested because
    # [*] this appends a dict to a list in a dictionary, instead
    # [*] of just modifying a key inside of a dictionary

    # 1. LOAD THE USER DATA
    user = sl.load(imp.user_data_toml)

    # 2. MODIFY IT TO ADD THE NEW CARD
    user["user"]["attack"].append(dict(card))

    # 3. SAVE THE USER DATA
    sl.save(user, imp.user_data_toml)


def print_card(card: dict) -> None:
    '''
    Print a given card to the console.

    :param card: A dictionary in the correct format for the card
    :type card: dict

    :rtype: None
    '''

    # This uses the inputted dictionary 
    # to show the card info to the user
    print(styles.format_style(f"""┌───────────────┐
{card["name"]}
DMG: {card["damage"]}
MANA: {card["mana_cost"]}
TOK: {card["cost"]}
TYPE: {card["type"]}
└───────────────┘
DESC: {card["desc"]}""", "bold_cyan"))

def create_opponent(diff: int) -> Opponent:
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
    for card in cards["atk"]:
        if int(cards["atk"][card]["diff"]) == diff:
            cards_in_diff.append(cards["atk"][card])

    # Collect a sample of 4 from the cards in diff list
    # and add them to the deck
    rand_atk_cards = random.sample(list(cards_in_diff), 4)
    for card in rand_atk_cards:
        deck.append(card)

    # Do the same for weapons
    cards_in_diff = []
    for card in cards["wpn"]:
        if int(cards["wpn"][card]["diff"]) == diff:
            cards_in_diff.append(cards["wpn"][card])

    rand_wpn_cards = random.sample(list(cards_in_diff), 2)
    for card in rand_wpn_cards:
        deck.append(card)

    # Do the same for armor
    cards_in_diff = []
    for card in cards["amr"]:
        if int(cards["amr"][card]["diff"]) == diff:
            cards_in_diff.append(cards["amr"][card])

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

    # 7. SET UP THE OPPONENT CLASS
    opponent = Opponent(
        diff, name, health, 
        rew, deck, tok_rew
    )

    # 8. RETURN THE OPPONENT
    return opponent

def clear() -> None:
    '''
    Quickly and efficiently clears the screen

    :rtype: None
    '''

    subprocess.run("cls", shell=True)

def quit(code:str | int) -> None:
    '''
    Exits with exit code 0

    :param code: The exit code for the program
    :type code: str | int

    :rtype: None
    '''

    sys.exit(code)
