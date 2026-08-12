from .opponent import Opponent

import util.styles as styles
import util.help_func as helper
import util.sl as sl
import util.key_vars as keyvars

import readchar
import random
import time
from math import ceil

imp = keyvars.KeyVars()

def start_match(world: int, enemy: Opponent, number: int) -> bool:
    '''
    Play a match using an Opponent class.

    :param world: The world the user is in
    :type world: int

    :param enemy: The enemy the user is fighting against
    :type enemy: Opponent

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
    op_health_max = enemy.health
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
        defense_u = 0
        defense_e = 0
        crit_inc_u = 0
        crit_inc_e = 0

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
            if defense_u > 0: defense_u -= 1
            if defense_e > 0: defense_e -= 1

            if not skip_u:
                # 1b. Show player health & effects
                print("Health: " + health_colored)
                print("+DMG: " + str(damage_inc_u) + " | Poison: " + str(poison_u))
                print("+ Crit %: " + str(crit_inc_u)) 
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
                print("Enemy +DMG: " + str(damage_inc_e) + " | Enemy Poison: " + str(poison_e))
                print("+ Crit %: " + str(crit_inc_e)) 
                # 1f. Show player colored deck
                print(styles.format_style("ENEMY DECK:", "red"))
                for card in enemy.deck:
                    formatted_card = "| " + helper.format_card_line(card, cards)
                    if card in used_cards_e:
                        formatted_card += styles.format_style(" [USED]", "error")
                    print(formatted_card)
                print("-------------------")
                weaknesses = []
                for weakness in enemy.weak_el + enemy.weak_mat:
                    weaknesses.append(weakness)
                print(styles.format_style(f"WEAKNESSES: {', '.join(w.capitalize() for w in weaknesses) if weaknesses else styles.format_style("No weaknesses.", "red")}", "green"))
                resistances = []
                for resistance in enemy.res_el + enemy.res_mat:
                    resistances.append(resistance)
                print(styles.format_style(f"RESISTANCES: {', '.join(r.capitalize() for r in resistances) if resistances else styles.format_style("No resistances.", "green")}", "red"))
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
                        name = enemy.name

                        dmg_random1 = round(damage / 12) - random.randint(-3, 2)
                        dmg_random2 = round(damage / 10) + random.randint(-2, 3)
                        crit = True if random.randint(1, 100) <= user["user"]["stats"]["crit"] + crit_inc_u else False

                        # Randomize the damage
                        damage += random.randint(min(dmg_random1, dmg_random2), max(dmg_random1, dmg_random2))
                        if crit:
                            crit_perc = 1.5 + round(random.uniform(-0.2, 0.2), 1)
                            damage *= crit_perc

                        damage += damage_inc_u + poison_e

                        # Apply resistances and weaknesses (exclusive to player -> enemy attack)
                        type_ = target["type"]
                        weakness_ = False
                        resistance_ = False
                        if type_ in enemy.weak_el + enemy.weak_mat:
                            weakness_ = True
                            match type_:
                                case "fire": mult = imp.fire_weak + random.uniform(-0.1, 0.1)
                                case "water": mult = imp.water_weak + random.uniform(-0.05, 0.05)
                                case "earth": mult = imp.earth_weak + random.uniform(-0.2, 0.2)
                                case "sun": mult = imp.sun_weak + random.uniform(-0.3, 0.3)
                                case "nature": mult = imp.nature_weak + random.uniform(-0.05, 0.05)
                                case _: mult = 1
                        elif type_ in enemy.res_el + enemy.res_mat:
                            resistance_ = True
                            match type_:
                                case "fire": mult = imp.fire_res + random.uniform(-0.1, 0.1)
                                case "water": mult = imp.water_res + random.uniform(-0.05, 0.05)
                                case "earth": mult = imp.earth_res + random.uniform(-0.2, 0.2)
                                case "sun": mult = imp.sun_res + random.uniform(-0.3, 0.3)
                                case "nature": mult = imp.nature_res + random.uniform(-0.05, 0.05)
                                case _: mult = 1
                        else: mult = 1

                        damage *= mult

                        match enemy.diff:
                            case 1: name = styles.format_style(name, "green")
                            case 2: name = styles.format_style(name, "cyan")
                            case 3: name = styles.format_style(name, "yellow")
                            case 4: name = styles.format_style(name, "progress")
                            case 5: name = styles.format_style(name, "red")

                        type_formatted = type_
                        match type_:
                            case "fire": type_formatted = styles.format_style(type_formatted, "red")
                            case "water": type_formatted = styles.format_style(type_formatted, "cyan")
                            case "earth": type_formatted = styles.format_style(type_formatted, "yellow")
                            case "sun": type_formatted = styles.format_style(type_formatted, "error")
                            case "nature": type_formatted = type_formatted
                            case _: type_formatted = type_formatted
                        
                        helper.clear()

                        def_div = 2 + random.uniform(-0.4, 0.1)
                        if defense_e: damage /= def_div

                        damage = ceil(damage)

                        op_health -= damage

                        mods = []
                        if damage_inc_u: damage_plus = f"+{damage_inc_u} DMG INC."; mods.append(damage_plus)
                        if poison_e: poison_plus = f"+{poison_e} POISON"; mods.append(poison_plus)

                        modifs: str = ', '.join(mod for mod in mods)

                        print(f"You played {helper.format_card_line(target_id, cards)}{styles.clear_styles()}!")
                        print(f"{name}{styles.clear_styles()} took {styles.format_style(str(damage), "red")} damage! {"(" if modifs != "" else ""}{modifs}{")" if modifs != "" else ""}")
                        if defense_e: print(f"The enemy defended! (card base dmg / {def_div})")
                        if crit: print(f"You got a {styles.format_style("critical hit", "red")}{styles.clear_styles()} on {name}{styles.clear_styles()} (x{crit_perc})")
                        if weakness_: print(f"You hit {name}{styles.clear_styles()}'s {styles.format_style("weakness", "green")}{styles.clear_styles()}! ({type_formatted.capitalize()}{styles.clear_styles()})")
                        if resistance_: print(f"You hit {name}{styles.clear_styles()}'s {styles.format_style("resistance", "red")}{styles.clear_styles()}... ({type_formatted.capitalize()}{styles.clear_styles()})")

                        time.sleep(3)
                    case "WPN":
                        # 3. APPLY EFFECTS
                        effect = target["effect"]
                        effects = helper.parse_effect(effect)

                        helper.clear()
                        print(f"You played {helper.format_card_line(target_id, cards)}{styles.clear_styles()}!")
                        for effect_type, value in effects.items():
                            match effect_type:
                                # 3a. Damage Increases
                                case "damage_increase": 
                                    damage_inc_u += value
                                    print(f"Your {styles.format_style("damage", "red")}{styles.clear_styles()} was increased! (+{value}, total +{damage_inc_u})")
                                    time.sleep(3)
                                # 3b. Poisoning
                                case "poison": 
                                    poison_e += value + 1
                                    print(f"You {styles.format_style("poisoned", "progress")}{styles.clear_styles()} the enemy! (+{value} poison, total {poison_e - 1})")
                                    time.sleep(3)
                                # 3c. Player turn skip
                                case "skip_enemy_turn": skip_e += value

                        if target["type"] in enemy.weak_el + enemy.weak_mat:
                            match target["type"]:
                                case "blade": additive = 3 * (imp.blade_weak + random.uniform(-0.15, 0.15))
                                case "blunt": additive = 3 * (imp.blunt_weak + random.uniform(-0.05, 0.05))
                                case "hard": additive = 3 * (imp.hard_weak + random.uniform(-0.4, 0.05))
                                case "wood": additive = 3 * (imp.wood_weak + random.uniform(-0.1, 0.1))
                                case _: additive = 1
                            additive = ceil(additive)
                            op_health -= additive
                            print(f"Opponent took {additive} damage due to being weak to {target["type"]}!")
                            time.sleep(3)
                        elif target["type"] in enemy.res_el + enemy.res_mat:
                            op_health += 5
                            print(f"Opponent gained {styles.format_style("5 health", "green")}{styles.clear_styles()} due to being resistant of {target["type"]}!")
                            time.sleep(3)

                    case "AMR":
                        # 3. APPLY EFFECTS
                        effect = target["effect"]
                        effects = helper.parse_effect(effect)

                        helper.clear()
                        print(f"You played {helper.format_card_line(target_id, cards)}{styles.clear_styles()}!")
                        for effect_type, value in effects.items():
                            match effect_type:
                                # 3a. Health Temp Inc
                                case "health_temp_increase":
                                    u_health += value
                                    print(f"Your health increased by {styles.format_style("+", "green")}{styles.format_style(str(value), "green")}{styles.clear_styles()}! (HP: {u_health})")
                                    time.sleep(3)
                                case "defend_round":
                                    defense_u += value
                                    print(f"You're now {styles.format_style("defending", "cyan")}{styles.clear_styles()} for {value} rounds!")
                                    time.sleep(3)
                                case "crit_inc":
                                    crit_inc_u += value
                                    print(f"Crit % increased by {styles.format_style(str(value), "green")}{styles.clear_styles()}!")
                                    time.sleep(3)

                        if target["type"] in enemy.weak_el + enemy.weak_mat:
                            match target["type"]:
                                case "metal": additive = 3 * (imp.metal_weak + random.uniform(-0.1, 0.3))
                                case "chain": additive = 3 * (imp.chain_weak + random.uniform(-0.07, 0.07))
                                case _: additive = 1
                            additive = ceil(additive)
                            op_health -= additive
                            print(f"Opponent took {additive} damage due to being weak to {target["type"]}!")
                            time.sleep(3)
                        elif target["type"] in enemy.res_el + enemy.res_mat:
                            additive = 5 + random.randint(-1, 1)
                            op_health += additive
                            print(f"Opponent gained {styles.format_style(f"{additive} health", "green")}{styles.clear_styles()} due to being resistant of {target["type"]}!")
                            time.sleep(3)

                if op_health <= 0: win = True; break

                # 4. CHECK FOR DECK USAGE
                if set(used_cards_u) == set(playable_cards):
                    # [;] Deck is used up, reshuffle
                    helper.clear()
                    print("Deck empty. " + styles.format_style("Reshuffling...", "progress"))
                    
                    used_cards_u = []
                    time.sleep(2)
            else:
                helper.clear()
                print("Your turn was skipped!")
                skip_u -= 1
                time.sleep(2)

            if skip_e: skip_e -= 1; print("Enemy turn was skipped!"); time.sleep(2); continue

            # 5. ENEMY TURN
            # Select the category to play
            enemy_atks = []
            enemy_wpns = []
            enemy_amrs = []
            # Get how many of each category there is
            for card_id in enemy.deck:
                match card_id[3:6].upper():
                    case "ATK": 
                        if not card_id in used_cards_e: enemy_atks.append(card_id)
                    case "WPN": 
                        if not card_id in used_cards_e: enemy_wpns.append(card_id)
                    case "AMR": 
                        if not card_id in used_cards_e: enemy_amrs.append(card_id)
            # Calculate percentages for each category
            atk_percent = len(enemy_atks) / len(enemy.deck)
            wpn_percent = len(enemy_wpns) / len(enemy.deck) 
            amr_percent = len(enemy_amrs) / len(enemy.deck)

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
                    e_name = enemy.name

                    dmg_random1 = round(damage / 12) - random.randint(-3, 2)
                    dmg_random2 = round(damage / 10) + random.randint(-2, 3)
                    crit = True if random.randint(1, 100) <= enemy.crit + crit_inc_e else False

                    # Randomize the damage
                    damage += random.randint(min(dmg_random1, dmg_random2), max(dmg_random1, dmg_random2))
                    if crit:
                        crit_perc = 1.5 + round(random.uniform(-0.2, 0.2), 1)
                        damage *= crit_perc

                    damage += damage_inc_e + poison_u

                    match enemy.diff:
                        case 1: e_name = styles.format_style(e_name, "green")
                        case 2: e_name = styles.format_style(e_name, "cyan")
                        case 3: e_name = styles.format_style(e_name, "yellow")
                        case 4: e_name = styles.format_style(e_name, "progress")
                        case 5: e_name = styles.format_style(e_name, "red")

                    helper.clear()

                    def_div = 2 + random.uniform(-0.4, 0.1)
                    if defense_u: damage /= def_div

                    mods = []
                    if damage_inc_e: damage_plus = f"+{damage_inc_e} DMG INC."; mods.append(damage_plus)
                    if poison_u: poison_plus = f"+{poison_u} POISON"; mods.append(poison_plus)

                    modifs: str = ', '.join(mod for mod in mods)

                    damage = ceil(damage)

                    if u_health - damage >= 10: u_health -= damage
                    else: u_health = 10

                    print(f"{e_name}{styles.clear_styles()} played {helper.format_card_line(enemy_card, cards)}{styles.clear_styles()}!")
                    print(f"You took {styles.format_style(str(damage), "red")} damage! {"(" if modifs != "" else ""}{modifs}{")" if modifs != "" else ""}")
                    if defense_u: print(f"You defended! (card base dmg / {def_div})")
                    if crit: print(f"{e_name}{styles.clear_styles()} hit you with a {styles.format_style("critical hit!", "red")}{styles.clear_styles()} (x{crit_perc})")
                    time.sleep(3)
                case "WPN":
                    # 3. APPLY EFFECTS
                    effect = target["effect"]
                    effects = helper.parse_effect(effect)

                    helper.clear()
                    print(f"Enemy played {helper.format_card_line(enemy_card, cards)}{styles.clear_styles()}!")
                    for effect_type, value in effects.items():
                        match effect_type:
                            # 3a. Damage Increases
                            case "damage_increase": 
                                damage_inc_e += value
                                print(f"Enemy damage was increased! (+{value}, total +{damage_inc_e})")
                                time.sleep(3)
                            # 3b. Poisoning
                            case "poison": 
                                poison_u += value + 1
                                print(f"Enemy poisoned you! (+{value}, total {poison_u - 1})")
                                time.sleep(3)
                            # 3c. Player turn skip
                            case "skip_enemy_turn": skip_u += value
                case "AMR":
                    # 3. APPLY EFFECTS
                    effect = target["effect"]
                    effects = helper.parse_effect(effect)
                    
                    helper.clear()
                    print(f"Enemy played {helper.format_card_line(enemy_card, cards)}{styles.clear_styles()}!")
                    for effect_type, value in effects.items():
                        match effect_type:
                            # 3a. Health Temp Inc
                            case "health_temp_increase":
                                op_health += value
                                print(f"Enemy health increased by {styles.format_style("+", "green")}{styles.format_style(str(value), "green")}{styles.clear_styles()}! (HP: {op_health})")
                                time.sleep(3)
                            case "defend_round":
                                defense_e += value
                                print(f"Enemy is now {styles.format_style("defending", "cyan")}{styles.clear_styles()} for {value} rounds!")
                                time.sleep(3)
                            case "crit_inc":
                                crit_inc_e += value
                                print(f"Enemy crit % increased by {styles.format_style(str(value), "green")}{styles.clear_styles()}!")
                                time.sleep(3)

            # Enemy reshuffling
            if set(used_cards_e) == set(enemy.deck):
                # [;] Enemy deck is used up, reshuffle
                helper.clear()
                used_cards_e = []

            if u_health <= 0: win = False; break
        if win:
            helper.clear()
            print(styles.format_style("You Won!", "success"))
            print("Press any key to continue...")
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

def start_exhibition(opp: Opponent) -> bool:
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
