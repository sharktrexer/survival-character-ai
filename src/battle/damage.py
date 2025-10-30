'''
Types of damage dealt by status effects, and actions:

    Physical damage: attacks with Str + other stats depending on situation, DEF resists
    Healing: heals with Rec, HP improves
    Evasion damage: attacks with Dex, EVA resists
    Magical damage: attacks with Int, REC resists
    Psychological damage: attacks with Cha, CHA + REC resists
    Fear damage: attacks with Itmd, FEAR resists
    Stress damage: attacks with Cha or Itmd, TRES resists 

Gear or special moves can add other stat values to any damage
'''
class Damage:
    def __init__(self, amount:int, 
                 empowering_stat_name:str, 
                 resisting_stat_name:str,
                 associated_element_name:str=None):
        '''
        Parameters:
            amount (int): amount of damage to deal
            empowering_stat_name (str): name of stat of the using peep to empower the attack
            resisting_stat_name (str): name of stat of a peep to resist the attack
            associated_element_name (str): element of the attack
        '''
        self.amount = amount
        self.empowering_stat = empowering_stat_name
        self.resisting_stat = resisting_stat_name
        self.element = associated_element_name