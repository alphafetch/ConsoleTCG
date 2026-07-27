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

    nested_success = sl.modify_nested(["user", "stats", "new_game"], 0, imp.user_data_toml)
    if nested_success:
        # [!] Edit was successful, continue with game()
        return True
    else:
        # [;] Edit failed (handled in game())
        return False