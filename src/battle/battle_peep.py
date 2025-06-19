from .stats import Stat, StatBoard

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
        return self.name + "\n" + self.stats
    
    def get_stat_apts(self):
        return StatBoard.get_stat_apts()
    
    def get_stat_tvs(self):
        return StatBoard.get_stat_tvs()
     
    def initiative(self):
        return StatBoard.initiative()
        
    def start(self, anchor_init:int):
        #TODO: Add start logic
        #TODO: a battle info obj should be passed in instead of just the anchor_init val
        pass 
    
    def turn(self):
        #TODO: Add turn logic
        
        pass
     
    ''' Gained extra energy from initiative calculations. 
    Reset vars and obtain an energy bonus
    '''   
    def energy_bonus(self):
        #TODO: should battle manager handle this???
        self.init_growth = 0
        self.gained_ap_bonus = True
        print(self.name + " - Gained energy bonus from initiative! Growth reset :O")
        #TODO: Add energy bonus to AP value
        