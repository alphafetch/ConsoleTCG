from typing import Any

class Opponent():
    def __init__(self, diff: int, name: str, health: int, reward: str, deck: list[str], 
                 tokens: int, xp: int, id: int, weak_el: list[str], res_el: list[str], 
                 weak_mat: list[str], res_mat: list[str], crit: int) -> None:
        '''
        Initialize an opponent.

        :param diff: The difficulty of the opponent
        :type diff: int

        :param name: The name of the opponent
        :type name: str

        :param health: The health of the opponent
        :type health: int
        
        :param reward: The card reward after defeating the opponent
        :type reward: str

        :param deck: A list of the opponent's deck
        :type deck: list[str]

        :param tokens: Tokens when defeating the enemy
        :type tokens: int

        :param xp: The XP when defeating the enemy
        :type xp: int

        :param id: The ID of the opponent
        :type id: int

        :param weak_el: The elemental weaknesses of an opponent
        :type weak_el: list[str]
        
        :param res_el: The elemental resistances of an opponent
        :type res_el: list[str]

        :param weak_mat: The material weaknesses of an opponent
        :type weak_mat: list[str]
        
        :param res_mat: The material resistances of an opponent
        :type res_mat: list[str]

        :param crit: The crit chance an opponent has
        :type crit: int

        :rtype: None
        '''

        self.diff = diff
        self.name = name
        self.health = health
        self.reward = reward
        self.deck = deck
        self.tokens = tokens
        self.xp = xp
        self.id = id
        self.weak_el = weak_el
        self.res_el = res_el
        self.weak_mat = weak_mat
        self.res_mat = res_mat