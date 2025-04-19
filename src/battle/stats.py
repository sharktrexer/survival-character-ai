
class Stat:
    def __init__(self, name:str, val:int, apt:int):
        self.name = name
        self.value = val
        self.apt = apt
        self.tv = self.calc_true_value()
        
    def calc_true_value(self):
        
        apt = self.apt
        val = self.value
        
        # 25% increments when positive (add to value after multiplication)
        if apt >= 0:
            mult = apt * 0.25 
            return val + int(val * mult)
        # 12.5% decrements when negative (multiplying by decimal for division)
        #  -1     -2    -3    -4
        # 0.875, 0.75, 0.625, 0.5
        if apt < 0:
            mult = 1 - (abs(apt) * 0.125)
            return int(val * mult)
            
class StatContainer:
    def __init__(self, stats:dict):
        self.stats = stats
        
    ''' Returns proper stat name from abreviation
    
    Example
    -------------
    input key: "strength" "Strength" "str", "STR"
    output: all turn into "Strength"
    
    '''
    def elongate_stat_abreviation(self, abre:str):
        if abre in ["s", "str", "strength"]:
            return "Strength"
        elif abre in ["d", "def", "defense"]:
            return "Defense"
        elif abre in ["e", "eva", "evasion"]:
            return "Evasion"
        elif abre in ["dx", "dex", "dexterity"]:
            return "Dexterity"
        elif abre in ["r", "rec", "recovery"]:
            return "Recovery"
        elif abre in ["i", "int", "intellect"]:
            return "Intellect"
        elif abre in ["c", "cre", "creativity"]:
            return "Creativity"
        elif abre in ["f", "fear"]:
            return "Fear"
        elif abre in ["it", "itmd", "intimidation"]:
            return "Intimidation"
        elif abre in ["ch", "char", "charisma"]:
            return "Charisma"
        elif abre in ["ss", "tres", "stress"]:
            return "Stress"
        elif abre in ["h", "hp", "health"]:
            return "Health"
        elif abre in ["hu", "hun", "hunger"]:
            return "Hunger"
        elif abre in ["a", "ap", "energy"]:
            return "Energy"
        