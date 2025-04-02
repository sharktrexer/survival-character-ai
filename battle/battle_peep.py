from peep.character import Character

''' A version of character that can be used in battle '''
class BattlePeep(Character):
    def __init__(self, name: str, desc: str, stat_aps_dict: dict, stats_dict: dict):
        super().__init__(name, desc, stat_aps_dict)
        self.stats = stats_dict
        self.cur_stats = stats_dict
        self.init_growth = 0
        self.init_rounds_passed = 0
        
    def calc_cur_stats(self):
        for statN in self.stat_aps.keys():
            apt = self.stat_aps[statN]
            # with 8 ap stats are tripled 
            if apt >= 0:
                mult = apt * 0.25 
                self.cur_stats[statN] = self.stats[statN] + (self.stats[statN] * mult)
            # 0 to -4 should be 0 mult to 1/2 mult
            #   1      2     3     4
            # 0.875, 0.75, 0.625, 0.5
            if apt < 0:
                mult = 1 - (abs(apt) * 0.125)
                self.cur_stats[statN] = self.stats[statN] * mult
        
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
        
        
        