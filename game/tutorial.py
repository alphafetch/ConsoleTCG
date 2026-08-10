import util.sl as sl
import util.key_vars as keyvars
import util.scr as scr
import util.help_func as helper

# This contains important variables such as the user data directory
imp = keyvars.KeyVars()

def run() -> bool:
    '''
    Runs the tutorial.

    :return: Returns True if successful, False if the new_game edit fails
    :rtype: bool
    '''

    scr.scr_tutorial()

    helper.clear()

    scr.scr_starter_card()

    helper.clear()

    nested_success = sl.modify_nested(["user", "stats", "new_game"], False, imp.user_data_toml)
    nested_unlock = sl.modify_nested(["unlocks", "decks"], True, imp.user_data_toml)
    nested_career = sl.modify_nested(["unlocks", "career", "unlocked"], True, imp.user_data_toml)
    if nested_success and nested_unlock and nested_career:
        # [!] Edit was successful, continue with game()
        return True
    else:
        # [;] Edit failed (handled in game())
        return False