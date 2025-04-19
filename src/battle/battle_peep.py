from .stats import Stat

''' A version of character that is battle oriented '''
class BattlePeep():
    def __init__(self, name: str,  stats_dict: dict):
        self.name = name
        self.stats = stats_dict
        self.init_growth = 0
        self.init_rounds_passed = 0
        
    def __str__(self):
        return self.name + "\n" + self.stats
        
    def initiative(self):
        return self.stats["Dexterity"].tv + self.stats["Evasion"].tv
        
    def turn(self):
        self.init_rounds_passed += 1
     
    ''' Gained extra energy from initiative calculations. 
    Reset vars and obtain an energy bonus
    '''   
    def energy_bonus(self):
        self.init_rounds_passed = 0
        self.init_growth = 0
        print(self.name + "- Gained energy bonus from initiative!")
        