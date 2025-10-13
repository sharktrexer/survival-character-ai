from .stats import Stat, StatBoard, sn
from .alteration import Alteration
from enum import Enum, auto

''' A version of character that is battle oriented 
'''
class BattlePeep():
    def __init__(self, name: str,  stats_dict: dict):
        self.name = name
        self.stats = StatBoard(stats_dict)
        self.battle_handler = BattleHandler()
        self.init_growth = 0
        self.gained_ap_bonus = False
        
    def __str__(self):
        return self.name
    
    def get_info_as_str(self):
        peep_info = self.name + ":\n"
        peep_info += self.stats.get_stats_as_str()
        return peep_info
    
    def get_stat(self, name:str) -> Stat:
        '''
        given a name, returns the peep's current stat obj
        '''
        return self.stats.get_stat_cur(name)
    
    def get_stat_apts(self):
        return self.stats.get_stat_apts()
    
    def get_stat_avs(self):
        return self.stats.get_stat_active_value
     
    def initiative(self):
        return self.stats.initiative()
    
    def recieve_alt(self, alt: Alteration):
        self.stats.apply_alteration(alt)
        
    def cleanse_alt(self, alt: Alteration):
        self.stats.remove_alteration(alt)
        
    def start(self):
        #TODO: Add start logic
        # trigger all on start turn effects
        pass 
    
    def turn(self):
        # are we bleeding out?
        self.battle_handler.handle_bleeding_out()
        
        # time has passed for alterations
        self.stats.tick_alterations()
        
        if self.battle_handler.stance == Peep_State.KNOCKED_OUT:
            #TODO: extra logic for knocked out peeps
            # currently will ignore energy bonus 
            # could ignore getting input from ai or player
            # perhaps trigger a flag to "help me!" and attract NPCs to help
            return
        
        # apply energy bonus
        if self.gained_ap_bonus: self.stats.apply_init_ap_bonus()
        
        # restore ap value
        self.stats.resource_restore("ap")
     
     
    def end_turn(self):
        # revert energy bonus
        self.gained_ap_bonus = False
    
    def end_battle(self):
        # recover wih 10% health if knocked out at end of battle
        if self.battle_handler.stance == Peep_State.KNOCKED_OUT: 
            self.recover_from_battle_end()
        
        # let battle handler know    
        self.battle_handler.end_battle()   
        
    ''' Gained extra energy from initiative calculations. 
    Reset vars and obtain an energy bonus
    '''   
    def energy_bonus(self):
        #TODO: should battle manager handle this???
        self.init_growth = 0
        self.gained_ap_bonus = True
        
    def affect_hp(self, amount:int):
        if self.stats.resource_is_depleted('hp'): 
            #TODO: logic for affecting bleed out
            return
        
        depleted = self.stats.resource_change('hp', amount)
        
        # knock out
        if depleted:
            self.battle_handler.knock_out(self.stats.get_stat_cur('hp').val_active)
            # TODO: affect fear and/or stress. maybe hunger too?
            
    def recover_from_battle_end(self):
        self.stats.resource_set_to_percent('hp', 0.1)
        #TODO: is anything else needed?
 
 
class Peep_State(Enum):
    STANDARD = auto()
    FLYING = auto()
    PRONE = auto()
    HANGING = auto()
    KNOCKED_OUT = auto()
    DEAD = auto()
        
'''
    Is a part of a battle peep to store and manipulate extra situational info
''' 
class BattleHandler():
    def __init__(self):
        self.temp_health = 0
        self.evasion_health = 0
        self.bleed_out = 0
        self.status_effects = []
        self.stance = Peep_State.STANDARD
        
    def knock_out(self, max_hp:int):
        self.stance = Peep_State.KNOCKED_OUT
        self.bleed_out = max_hp
        
    def handle_bleeding_out(self):
        '''
        Returns:
            bool: if peep is dead from bleeding out
        '''
        if self.stance != Peep_State.KNOCKED_OUT:
            return
        
        # TODO: count down bleed out based on HP Apt
        # 5 for Apt 0, 15 at Apt 8, 3 for Apt -4
        
        if self.bleed_out <= 0:
            self.stance = Peep_State.DEAD
            return True
        
        return False
        
    def end_battle(self):
        # perhaps stance could be different if char is always flying
        self.stance = Peep_State.STANDARD
        self.bleed_out = 0
        self.evasion_health = 0
        # temp hp can potentially carry over out of battle
        
class Inventory():
    
    def __init__(self):
        self.equipped = []
        self.carrying = []
        
    def sort(self):
        pass
    
    def equip(self):
        pass
        
    def unequip(self):
        pass
    
    def add_item(self):
        pass
    
    def remove_item(self):
        pass
        
    