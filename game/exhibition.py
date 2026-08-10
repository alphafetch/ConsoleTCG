import util.scr as scr
import util.help_func as helper

from . import match

def start_exhibition() -> bool:
    '''
    Play an exhibition game against a set difficulty opponent.

    :return: Returns a boolean of if the user won or not
    :rtype: bool
    '''

    # Clear the screen
    helper.clear()

    # 1. GET THE DIFFICULTY THE PLAYER WANTS (INT)
    diff = scr.scr_diff_select_exhibition()

    if not diff in [1, 2, 3, 4, 5]:
        raise ValueError("Difficulty invalid.")

    # 3. PLAY THE MATCH
    opponent = helper.create_opponent(diff)

    match.start_exhibition(opponent)

    return True