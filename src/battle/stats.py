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
        
    def get_all_names(self):
        return [self.name, self.name.lower(), self.abreviation] + self.ex_names
        
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
   
STAT_TYPES = {
        "strength": Stat("strength", 0, 0, "str", ["s", "fuerza"]),
        "defense": Stat("defense", 0, 0, "def", ["d", "defensa"]),
        "evasion": Stat("evasion", 0, 0, "eva", ["e", "evasion"]),
        "dexterity": Stat("dexterity", 0, 0, "dex", ["dx", "destreza"]),
        "recovery": Stat("recovery", 0, 0, "rec", ["r", "recovery"]),
        "intelligence": Stat("intelligence", 0, 0, "int", ["i", "intellect", "inteligencia"]),
        "creativity": Stat("creativity", 0, 0, "cre", ["c", "create", "creatividad"]),
        "fear": Stat("fear", 0, 0, "fear", ["f", "spook", "miedo"]),
        "intimidation": Stat("intimidation", 0, 0, "itmd", ["it", "intim","intimidacion"]),
        "charisma": Stat("charisma", 0, 0, "cha", ["ch", "char", "carisma"]),
        "stress": Stat("stress", 0, 0, "tres", ["ss", "estres"]),
        "health": Stat("health", 0, 0, "hp", ["h", "health points", "salud", "puntos de salud"]),
        "hunger": Stat("hunger", 0, 0, "hun", ["hu", "hun", "hung", "hambre"]),
        "energy": Stat("energy", 0, 0, "ap", ["a", "action points", "energia", "puntos de accion"]),
}
 
def sn(name):
    """
    Returns the full name of a stat given a name, abreviation, or 
    any of the extra applicable names. Case insensitive. 
    Returns empty string if stat name not found.

    Parameters:
        name (str): name of stat

    Returns:
        str: full name of stat
    """
    full_name = ""
    for stat in STAT_TYPES.values():
        poss_names = stat.get_all_names()
        if name.lower() in poss_names:
            full_name = stat.name
            
    return full_name
            
def make_stat(name, val, apt):
        name = sn(name).lower()
        stat = STAT_TYPES[name]
        stat.apt = apt
        stat.value = val
        return stat

class StatBoard:
    def __init__(self):
        self.stats = STAT_TYPES
        
    