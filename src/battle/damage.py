'''
Types of damage dealt by status effects, and actions:

    Physical damage: attacks with stat dependant on weapon type, DEF resists
    Healing: heals with Rec, HP improves
    Magical damage: attacks with Int, REC resists
    
    Psychological damage: attacks with Cha, CHA + REC resists
    
    :::::::::::::Damage to Non-Health Points:::::::::::::
    Evasion damage: attacks with Dex onto Evasion Health, EVA resists
    Fear damage: attacks with Itmd onto Fear Health, FEAR resists
    Stress damage: attacks with Cha or Itmd onto Stress Health, TRES resists 
    
    Disgust Trauma: limits max hunger points
    

Gear or special moves can add other stat values to any damage
'''
from enum import Enum, auto


def create_dmg_preset(ratio:int, type:Damage.DamageType):
    '''
    Creates a specific damage object given the type
    
    EXCLUDES PHYSICAL
    '''
    match type:
        case Damage.DamageType.Physical:
            return Damage(ratio, 'str', 'def')
        case Damage.DamageType.Healing:
            return Damage(ratio, 'rec', 'hp', is_heal=True)
        case Damage.DamageType.Magical:
            return Damage(ratio, 'int', 'rec')
        case Damage.DamageType.Evasion:
            return Damage(ratio, 'dex', 'eva')
        case Damage.DamageType.Fear:
            return Damage(ratio, 'itmd', 'fear')
        case Damage.DamageType.Stress:
            return Damage(ratio, 'cha', 'tres')
        
def create_specific_phys_dmg(ratio:int, stat:str):
    return Damage(ratio, stat, 'def')
        

class Damage:
    
    class DamageType(Enum):
        Physical = auto()
        Healing = auto()
        Evasion = auto()
        Magical = auto()
        Psychological = auto()
        Fear = auto()
        Stress = auto()
    
    def __init__(self, ratio:int, 
                 empowering_stat: str,
                 resisting_stat_name:str,
                 associated_element_name:str='',
                 is_heal = False
                 ):
        '''
        Parameters:
            ratio (int): damage multiplier
            empowering_stat (str): stat that deals the damage
            resisting_stat_name (str): stat that is will resist the damage
            associated_element_name (str): element associated with the damage
            is_heal (bool): whether the damage is healing
        '''
        self.ratio = ratio
        self.empowering_stat = empowering_stat
        self.resisting_stat = resisting_stat_name
        self.element = associated_element_name
        self.is_heal = is_heal
        self.amount = 0
        
    def give_value(self, empowering_stat_av:int):
        '''
        Pass in empowering stat active value to store the damage amount
        
        Allows for an amount to have been previously set to add onto
        '''
        value = int(round(self.ratio * empowering_stat_av))
        if not self.is_heal:
            value *= -1 
        self.amount += value