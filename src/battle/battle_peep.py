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
    
    def get_stat(self, name:str):
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
        #TODO: a battle info obj should be passed in instead of just the anchor_init val
        pass 
    
    def turn(self):
        
        self.stats.tick_alterations()
        
        self.stats.reset_stat("ap")
        if self.gained_ap_bonus: self.stats.apply_init_ap_bonus()
        
        # temp print to test debuffs and buffs on one stat
        '''
        buffs = self.stats.get_all_buffs().values()
        if buffs:
            str_buffs = buffs[sn("Strength")]
            if str_buffs:
                print("this is my most potent strength buff: ", 
                    self.stats.str_buffs[0],
                    "\n",
                    "Rest: ", *str_buffs)
        
        debuffs = self.stats.get_all_debuffs()
        if debuffs:
            str_debuffs = debuffs[sn("Strength")]
            if str_debuffs:
                print("this is my most potent strength debuff: ", 
                    self.stats.str_debuffs[0],
                    "\n",
                    "Rest: ", *str_debuffs)
                '''
     
     
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
        #TODO: Add energy bonus to AP value
        