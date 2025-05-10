STAT_NAMES = [
        "Strength", "Defense", "Evasion",   
                
        "Dexterity", "Recovery", "Intelligence", 
        
        "Creativity", "Fear", "Intimidation",
        
        "Charisma", "Stress", "Health", 
        
        "Hunger", "Energy", 
    ]

class Stat:
    def __init__(self, name:str, val:int, apt:int, abreviation:str, ex_names:list):
        """
        Parameters:
            name (str): name of stat
            val (int): base value of stat
            apt (int): aptitude value of stat
            abreviation (str): abreviation of stat
            ex_names (list[str]): list of extra applicable names
        """
        
        self.name = name
        self.abreviation = abreviation
        self.ex_names = ex_names
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
            

class StatBoard:
    def __init__(self):
        self.stats = self.set_stats()
    
    def set_stats(self):
        stats = {}
        stats.append(Stat("strength", 0, 0, "str", ["s", "fuerza"]))
        stats.append(Stat("defense", 0, 0, "def", ["d", "defensa"]))
        stats.append(Stat("evasion", 0, 0, "eva", ["e", "evasion"]))
        stats.append(Stat("dexterity", 0, 0, "dex", ["dx", "destreza"]))
        stats.append(Stat("recovery", 0, 0, "rec", ["r", "recovery"]))
        stats.append(Stat("intelligence", 0, 0, "int", 
                          ["i", "intellect", "inteligencia"]))
        stats.append(Stat("creativity", 0, 0, "cre", 
                          ["c", "create", "creatividad"]))
        stats.append(Stat("fear", 0, 0, "Fear", ["f", "spook", "miedo"]))
        stats.append(Stat("intimidation", 0, 0, "itmd", ["it", "intimidacion"]))
        stats.append(Stat("charisma", 0, 0, "ch", ["ch", "char", "carisma"]))
        stats.append(Stat("stress", 0, 0, "tres", ["ss", "estres"]))
        stats.append(Stat("health", 0, 0, "hp", 
                          ["h", "health points", "salud", "puntos de salud"]))
        stats.append(Stat("hunger", 0, 0, "hun", ["hu", "hun", "hung", "hambre"]))
        stats.append(Stat("energy", 0, 0, "ap", 
                          ["a", "action points", "energia", "puntos de accion"]))
        
        return stats