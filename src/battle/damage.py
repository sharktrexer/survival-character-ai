'''
Types of damage dealt by status effects, and actions:

    Physical damage: attacks with stat dependant on weapon type, DEF resists
    Magical damage: attacks with Int, REC resists
        Also adds 0.5x Int to Dodge damage if evaded
    
    Psychological damage: attacks with Cha, CHA resists
    
    Applying Non-Psychological Ailments (Status Effects or Debuffs)
        Includes Physical or Magical related ailments
    
    All can be evaded by Dodge, where 1x Dex is used as damage against dodge
    
    :::::::::::::Cannot be Dodged:::::::::::::
    Healing: heals with Rec, HP improves
        Excluding Undead targets that take dmg from heals
    Stress Heal: heals with Tres +0.25x Rec, TRES improves
    Fear Heal: heals with Fear + 0.25x Rec, FEAR improves
    
    Applying Psychological Ailments 
        Includes Stress, Hunger, Fear, Intimidation, Charisma Debuffs
    
    Fear damage: attacks with Itmd onto Fear Health, FEAR resists
    Stress damage: attacks with stat onto Stress Health, TRES resists 
    
    Disgust Trauma: limits max hunger points
    
    Armor effects are determined by the defensive move used
        Thus it can potentially defend against anything
    
    

Gear or special moves can add other stat values to any damage
'''
from enum import Enum, auto


def create_dmg_preset(ratio:int, type:Damage.DamageType):
    '''
    Creates a simple damage object given the type
    '''
    match type:
        case Damage.DamageType.Physical:
            return Damage(ratio, 'str', 'def')
        case Damage.DamageType.Healing:
            return Damage(ratio, 'rec', 'hp', is_heal=True, evadable=False)
        case Damage.DamageType.Magical:
            return Damage(ratio, 'int', 'rec')
        case Damage.DamageType.Psychological:
            return Damage(ratio, 'cha', 'cha')

def create_gauge_dmg(ratio:int, type:Damage.DamageType, empower_stat:str, is_heal:bool=False):
        match type:
            case Damage.DamageType.Stress:
                if is_heal:
                    return Damage(ratio, 'tres', 'tres', is_heal=True, evadable=False)
                return Damage(ratio, empower_stat, 'tres', is_heal=False, evadable=False)
            case Damage.DamageType.Fear:
                if is_heal:
                    return Damage(ratio, 'fear', 'fear', is_heal=True, evadable=False)
                return Damage(ratio, 'itmd', 'fear', is_heal=False, evadable=False)

def create_status_dmg(ratio:int, type:Damage.DamageType):
    match type:
        case Damage.DamageType.Magical:
            return Damage(ratio, 'int', 'rec', evadable=False)
        
def create_specific_phys_dmg(ratio:int, stat:str):
    return Damage(ratio, stat, 'def')
        

class Damage:
    
    class DamageType(Enum):
        Physical = auto()
        Healing = auto()
        Magical = auto()
        Psychological = auto()
        Fear = auto()
        Stress = auto()
    
    def __init__(self, ratio:int, 
                 empowering_stat: str,
                 resisting_stat_name:str,
                 associated_element_name:str='',
                 is_heal = False,
                 evadable = True
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
        
        self.evadable = evadable
        
        self.mult = 1.0 #added through exterior classes | applies to amount value
        
    def give_value(self, empowering_stat_av:int):
        '''
        Pass in empowering stat active value to store the damage amount
        
        Allows for an amount to have been previously set to add onto
        '''
        value = int(round(self.ratio * empowering_stat_av * self.mult))
        if not self.is_heal:
            value *= -1 
        self.amount += value