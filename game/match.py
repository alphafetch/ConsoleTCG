from .opponent import Opponent

import util.styles as styles
import util.help_func as helper
import util.sl as sl
import util.key_vars as keyvars

from typing import Any
import readchar
import random
import time
from math import ceil

imp = keyvars.KeyVars()

def start_match(world: int, enemy: dict[str, Any], number: int) -> bool:
    '''
    Play a match using an Opponent class.

    :param world: The world the user is in
    :type world: int

    :param enemy: The enemy the user is fighting against
    :type enemy: dict[str, Any]

    :param number: The enemy's number in the world
    :type number: int

    :return: Returns if the user won or not
    :rtype: bool
    '''

    # Clear the screen
    helper.clear()

    # Load user data and opponent data (from object)
    user = sl.load(imp.user_data_toml)
    decks = sl.load(imp.user_decks_toml)
    cards = sl.load(imp.cards_toml)
    u_health_max = user["user"]["stats"]["max_hp"]
    op_health_max = enemy["health"]
    u_health = 0
    op_health = 0

    # Have user select a deck
    deck = None
    disallowed_decks = []

    deck1_empty = all(i == "empty" for i in decks["decks"]["deck1"]["cards"])
    deck2_empty = all(i == "empty" for i in decks["decks"]["deck2"]["cards"])
    deck3_empty = all(i == "empty" for i in decks["decks"]["deck3"]["cards"])
    if deck1_empty: disallowed_decks.append("1")
    if deck2_empty: disallowed_decks.append("2")
    if deck3_empty: disallowed_decks.append("3")

    deck_num = helper.clean_input("SELECT DECK # (1-3): ", ["1", "2", "3"], disallowed_decks, "That deck is empty. Select a different one.")
    deck = decks["decks"]["deck" + str(deck_num)]["cards"]

    # Heal both parties
    u_health = u_health_max
    op_health = op_health_max

    # Set used cards to none
    used_cards_u = []
    used_cards_e = []

    if world == 1:
        # Explain that this is a tutorial match
        print(styles.format_style("This is a tutorial match. There will only be one round.", "cyan"))
        print(styles.format_style("Press any key to start the match...", "warn"))
        readchar.readkey()

        damage_inc_e = 0
        damage_inc_u = 0
        poison_e = 0
        poison_u = 0
        skip_e = 0
        skip_u = 0

        # Loop until someone dies
        while True:
            # Clear the screen
            helper.clear()

            # 1. SHOW STATUS
            # 1a. Get player's health window
            if u_health >= 70:
                health_colored = styles.format_style(str(u_health), "green")
            elif u_health >= 21:
                health_colored = styles.format_style(str(u_health), "yellow")
            else:
                health_colored = styles.format_style(str(u_health), "red")

            if poison_u > 0: poison_u -= 1
            if poison_e > 0: poison_e -= 1

            if not skip_u:
                # 1b. Show player health & effects
                print("Health: " + health_colored)
                print("+DMG: " + str(damage_inc_u))
                print("Poison: " + str(poison_u))
                # 1c. Show player colored deck
                print(styles.format_style("DECK:", "bold_cyan"))
                for id, card in enumerate(deck):
                    formatted_card = f"| {id + 1}. " + helper.format_card_line(card, cards)
                    if str(id + 1) in used_cards_u:
                        formatted_card += styles.format_style(" [USED]", "error")
                    print(formatted_card)
                print("-------------------")
                # 1d. Get enemy's health window
                if op_health >= 70:
                    health_colored = styles.format_style(str(op_health), "green")
                elif op_health >= 21:
                    health_colored = styles.format_style(str(op_health), "yellow")
                else:
                    health_colored = styles.format_style(str(op_health), "red")

                # 1e. Show enemy health
                print("Enemy Health: " + health_colored)
                print("Enemy +DMG: " + str(damage_inc_e))
                print("Enemy Poison: " + str(poison_e))
                # 1f. Show player colored deck
                print(styles.format_style("ENEMY DECK:", "red"))
                for card in enemy["deck"]:
                    formatted_card = "| " + helper.format_card_line(card, cards)
                    if card in used_cards_e:
                        formatted_card += styles.format_style(" [USED]", "error")
                    print(formatted_card)
                print("-------------------")
                print(styles.format_style("YOUR TURN:", "cyan"))
                playable_cards = []
                # [*] all_cards is used here to get the correct error 
                # [*] message when trying to play an empty slot or used card.
                all_cards = []
                disallowed_cards = []
                for id, card in enumerate(deck):
                    if card != "empty":
                        all_cards.append(str(id + 1))
                        playable_cards.append(str(id + 1))
                    else:
                        all_cards.append(str(id + 1))
                        disallowed_cards.append(str(id + 1))
                for card in used_cards_u:
                    disallowed_cards.append(card)
                selected_card = helper.clean_input("Card to play (#): ", all_cards, disallowed_cards, "That card can't be played. Pick a different one.")

                # Map the user's selection
                used_cards_u.append(selected_card)    
                target_id = deck[int(selected_card) - 1]

                # 2. CHECK THE TARGET CATEGORY
                target_cat = target_id[3:6].upper()
                target = cards[target_cat][target_id]
                match target_cat:
                    case "ATK":
                        # 3. DAMAGE THE ENEMY
                        damage = int(target["damage"])
                        name = enemy["name"]

                        dmg_random1 = round(damage / 12) - random.randint(-3, 2)
                        dmg_random2 = round(damage / 10) + random.randint(-2, 3)
                        crit = True if random.randint(1, 100) <= user["user"]["stats"]["crit"] else False

                        # Randomize the damage
                        damage += random.randint(min(dmg_random1, dmg_random2), max(dmg_random1, dmg_random2))
                        if crit:
                            crit_perc = 1.5 + round(random.uniform(-0.2, 0.2), 1)
                            damage *= crit_perc

                        damage += damage_inc_u + poison_e

                        match enemy["diff"]:
                            case 1: name = styles.format_style(name, "green")
                            case 2: name = styles.format_style(name, "cyan")
                            case 3: name = styles.format_style(name, "yellow")
                            case 4: name = styles.format_style(name, "progress")
                            case 5: name = styles.format_style(name, "red")

                        helper.clear()

                        damage = ceil(damage)

                        op_health -= damage

                        print(f"You played {helper.format_card_line(target_id, cards)}{styles.clear_styles()}!")
                        print(f"{name}{styles.clear_styles()} took {styles.format_style(str(damage), "red")} damage!")
                        if crit: print(f"You got a {styles.format_style("critical hit", "red")}{styles.clear_styles()} on {name}{styles.clear_styles()} (x{crit_perc})")
                        time.sleep(1.5)
                    case "WPN":
                        # 3. APPLY EFFECTS
                        effect = target["effect"]
                        effects = helper.parse_effect(effect)
                        
                        for effect_type, value in effects.items():
                            match effect_type:
                                # 3a. Damage Increases
                                case "damage_increase": 
                                    damage_inc_u += value
                                    helper.clear()
                                    print(f"Your damage was increased! (+{value}, total +{damage_inc_u})")
                                    time.sleep(1.5)
                                # 3b. Poisoning
                                case "poison": 
                                    poison_e += value
                                    helper.clear()
                                    print(f"You poisoned the enemy! (+{value} poison, total {poison_e})")
                                    time.sleep(1.5)
                                # 3c. Player turn skip
                                case "skip_enemy_turn": skip_e += value
                    case "AMR":
                        # 3. APPLY EFFECTS
                        effect = target["effect"]

                if op_health <= 0: win = True; break

                # 4. CHECK FOR DECK USAGE
                if set(used_cards_u) == set(playable_cards):
                    # [;] Deck is used up, reshuffle
                    helper.clear()
                    print("Deck empty. " + styles.format_style("Reshuffling...", "progress"))
                    
                    used_cards_u = []
                    time.sleep(1.5)
            else:
                helper.clear()
                print("Your turn was skipped!")
                skip_u -= 1
                time.sleep(1.5)

            if skip_e: skip_e -= 1; print("Enemy turn was skipped!"); time.sleep(1.5); continue

            # 5. ENEMY TURN
            # Select the category to play
            enemy_atks = []
            enemy_wpns = []
            enemy_amrs = []
            # Get how many of each category there is
            for card_id in enemy["deck"]:
                match card_id[3:6].upper():
                    case "ATK": 
                        if not card_id in used_cards_e: enemy_atks.append(card_id)
                    case "WPN": 
                        if not card_id in used_cards_e: enemy_wpns.append(card_id)
                    case "AMR": 
                        if not card_id in used_cards_e: enemy_amrs.append(card_id)
            # Calculate percentages for each category
            atk_percent = len(enemy_atks) / len(enemy["deck"])
            wpn_percent = len(enemy_wpns) / len(enemy["deck"]) 
            amr_percent = len(enemy_amrs) / len(enemy["deck"])

            # Decide which category to use a card from
            # [*]                                  V This list has the options to select based on the weights
            # [*]                                                           V These are the weights to select the first list by
            enemy_card_category = random.choices(["ATK", "WPN", "AMR"], weights=[atk_percent, wpn_percent, amr_percent], k=1)[0] # < This does a weighted selection on what category to choose

            # Select a card from the category
            match enemy_card_category:
                case "ATK": enemy_card = random.choice(enemy_atks)
                case "WPN": enemy_card = random.choice(enemy_wpns)
                case "AMR": enemy_card = random.choice(enemy_amrs)

            used_cards_e.append(enemy_card)
            target = cards[enemy_card_category][enemy_card]
            match enemy_card_category:
                case "ATK":
                    # 3. DAMAGE THE PLAYER
                    damage = int(target["damage"])
                    name = "You"
                    e_name = enemy["name"]

                    dmg_random1 = round(damage / 12) - random.randint(-3, 2)
                    dmg_random2 = round(damage / 10) + random.randint(-2, 3)
                    crit = True if random.randint(1, 100) <= enemy["crit"] else False

                    # Randomize the damage
                    damage += random.randint(min(dmg_random1, dmg_random2), max(dmg_random1, dmg_random2))
                    if crit:
                        crit_perc = 1.5 + round(random.uniform(-0.2, 0.2), 1)
                        damage *= crit_perc

                    damage += damage_inc_e + poison_u

                    match enemy["diff"]:
                        case 1: e_name = styles.format_style(e_name, "green")
                        case 2: e_name = styles.format_style(e_name, "cyan")
                        case 3: e_name = styles.format_style(e_name, "yellow")
                        case 4: e_name = styles.format_style(e_name, "progress")
                        case 5: e_name = styles.format_style(e_name, "red")

                    helper.clear()

                    damage = ceil(damage)

                    if u_health - damage >= 10: u_health -= damage
                    else: u_health = 10

                    print(f"{e_name}{styles.clear_styles()} played {helper.format_card_line(enemy_card, cards)}{styles.clear_styles()}!")
                    print(f"{name} took {styles.format_style(str(damage), "red")} damage!")
                    if crit: print(f"{e_name}{styles.clear_styles()} hit you with a {styles.format_style("critical hit!", "red")}{styles.clear_styles()} (x{crit_perc})")
                    time.sleep(1)
                case "WPN":
                    # 3. APPLY EFFECTS
                    effect = target["effect"]
                    effects = helper.parse_effect(effect)

                    for effect_type, value in effects.items():
                        match effect_type:
                            # 3a. Damage Increases
                            case "damage_increase": 
                                damage_inc_e += value
                                helper.clear()
                                print(f"Enemy damage was increased! (+{value}, total +{damage_inc_e})")
                                time.sleep(1.5)
                            # 3b. Poisoning
                            case "poison": 
                                poison_u += value
                                helper.clear()
                                print(f"Enemy poisoned you! (+{value}, total {poison_u})")
                                time.sleep(1.5)
                            # 3c. Player turn skip
                            case "skip_enemy_turn": skip_u += value
                case "AMR":
                    # 3. APPLY EFFECTS
                    effect = target["effect"]
                    effects = helper.parse_effect(effect)

            # Enemy reshuffling
            if set(used_cards_e) == set(enemy["deck"]):
                # [;] Enemy deck is used up, reshuffle
                helper.clear()
                used_cards_e = []

            if u_health <= 0: win = False; break
        if win:
            helper.clear()
            print(styles.format_style("You Won!", "success"))
            print("Press any key to continue...")
            sl.modify_nested(["unlocks", "career", "progress", "world" + str(world), str(number)], True, imp.user_data_toml)
            readchar.readkey()
        else:
            helper.clear()
            print(styles.format_style("You Lost...", "red"))
            print("Press any key to continue...")
            readchar.readkey()

        return win
    else:
        for i in range(3):
            # Loop until someone dies
            while True:
                break # STUB

        win = True
        return win

def start_exhibition(opp: Opponent) -> bool: # TODO Exhibition match
    '''
    Play a match using an Opponent class.

    :param opp: The opponent to play against
    :type opp: Opponent

    :return: Returns if the user won or not
    :rtype: bool
    '''

    # Clear the screen
    helper.clear()

    # Load user data and opponent data (from object)
    user = sl.load(imp.user_data_toml)
    u_health_max = user["user"]["stats"]["max_hp"]
    op_health_max = opp.health
    u_health = 0
    op_health = 0

    for i in range(3):
        # Heal both parties
        u_health = u_health_max
        op_health = op_health_max

        # Loop until someone dies
        while True:
            break # STUB
