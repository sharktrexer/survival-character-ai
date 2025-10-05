from .stats import Stat, StatBoard, sn
from .alteration import Alteration

''' A version of character that is battle oriented 
TODO: contain innitiative related stats into its own class
class for containing functions versus game logic?
'''
class BattlePeep():
    def __init__(self, name: str,  stats_dict: dict):
        self.name = name
        self.stats = StatBoard(stats_dict)
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
        pass 
    
    def turn(self):
        
        self.stats.tick_alterations()
        
        self.stats.resource_restore("ap")
        if self.gained_ap_bonus: self.stats.apply_init_ap_bonus()
     
     
    def end_turn(self):
        # revert energy bonus
        self.gained_ap_bonus = False
        
     
    ''' Gained extra energy from initiative calculations. 
    Reset vars and obtain an energy bonus
    '''   
    def energy_bonus(self):
        #TODO: should battle manager handle this???
        self.init_growth = 0
        self.gained_ap_bonus = True
        