''' A version of character that is battle oriented '''
class BattlePeep():
    def __init__(self, name: str,  stats_dict: dict):
        self.name = name
        self.stats = stats_dict
        self.init_growth = 0
        self.init_rounds_passed = 0
        
    def initiative(self):
        return self.cur_stats["Dexterity"] + self.cur_stats["Evasion"]
        
    def turn(self):
        self.init_rounds_passed += 1
     
    ''' Gained extra energy from initiative calculations. 
    Reset vars and obtain an energy bonus
    '''   
    def energy_bonus(self):
        self.init_rounds_passed = 0
        self.init_growth = 0
        print("Gained energy bonus from initiative!")
        