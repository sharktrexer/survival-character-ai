import copy
import math

from battle.alteration import Alteration, ap_buff

'''
                         APTITUDE UTILITIES
'''

def get_mult_of_aptitude(apt):
    
    """
    Aptitudes range from -4 to 8, with -4 being the most negative and 8 being the most positive.
    Positive Aptitudes increase mult stat values by 25% from 1 for each aptitude above 0
    Negative Aptitudes decrease mult by 12.5% from 1 for each aptitude below 0.
    Aptitiude of 0 has a mult of 1

    Parameters:
        apt (int): Aptitude of the stat

    Returns:
        float: Multiplier of the stat's aptitude
    """
    if apt < -4 or apt > 8:
        raise ValueError("Aptitude must be between -4 and 8")
    
    # 25% increments when positive 
    #   1      2     3     4  etc...  8
    #  1.25   1.5   1.75   2          3
    if apt >= 0:
        return (apt * 0.25) + 1
    # 12.5% decrements when negative 
    #  -1     -2    -3    -4
    # 0.875, 0.75, 0.625, 0.5
    else:
        return 1 - (abs(apt) * 0.125)

'''
                         APTITUDE LEVELING
'''

XP_REQURED_PER_APT = {}

def populate_xp_dict():
    """
    Fills in the XP_REQURED_PER_APT dict with the required XP
    to reach each aptitude level using the MAX_POINTS_TO_LEVEL integer.
    
    The current XP requirement formula is as follows:
        - From -4 to -1: 0, point_inc, then point_inc / 2 + previous value every iteration
        - From 1 to 8: point_inc * 2 + previous value every iteration
        (point_inc is a copy of MAX_POINTS_TO_LEVEL)
    """
    
    # baseline
    XP_REQURED_PER_APT[-4] = 0
    
    MAX_POINTS_TO_LEVEL = 40
    
    point_inc = MAX_POINTS_TO_LEVEL
    
    for i in range(-3, 9):
        
        XP_REQURED_PER_APT[i] = point_inc + XP_REQURED_PER_APT[i-1]
        
        if i < 0:
            point_inc = int(point_inc / 2)    
        elif i > 0:
            point_inc = (point_inc * 2 if point_inc < MAX_POINTS_TO_LEVEL 
                         else MAX_POINTS_TO_LEVEL) 
    
populate_xp_dict()

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
        
        # Naming
        self.name = name
        self.abreviation = abreviation
        self.ex_names = ex_names
        
        # Numericals
        self.value = val
        self.apt = apt
        self.apt_exp = 0 
        self.av = 0
        self.multiplier = 1.0
        
        # Alterations
        self.buffs = []
        self.debuffs = []
        
        #TODO: should this class have a way to point to its battlepeep owner?
        
    def __str__(self):
        return (f"{self.name.upper()}: \nApt - {self.apt:<3} Val - {self.value:<4} Active Val - {self.av:<4}" 
                + f"\nCurrent Modifier - {self.multiplier:<4}"
                + f"\nCurrent Apt Exp - {self.apt_exp:<4} Exp to Next Level - {self.get_xp_req_to_next_apt_level():<4}")
    
    ''' 
                                HELPER FUNCTIONS
    ''' 
    def print_simple_str(self):
        return f"{self.name.upper()}: \nApt - {self.apt:<3} Val - {self.value:<4} Active Val - {self.av:<4}" 
    
    def get_all_names(self):
        return [self.name, self.name.lower(), self.abreviation] + self.ex_names
    
    def get_xp_req_to_next_apt_level(self):
        if self.apt == 8: return 0
        
        return XP_REQURED_PER_APT[self.apt + 1] - self.apt_exp
    
    ''' 
                            ACTIVE VALUE CALCULATION
    '''
    def reset_to(self, val:int, apt:int):
        self.buffs = []
        self.debuffs = []
        self.set_new_vals(val, apt)
       
    def set_new_vals(self, val:int, apt:int):
        self.value = int(val)
        self.apt = int(apt)
        self.calc_active_value()
    
    def calc_active_value(self):
        # reset
        self.multiplier = 1
        
        # add apt multiplier
        self.multiplier *= get_mult_of_aptitude(self.apt)
        
        # ADD OTHER MULTIPLIERS HERE
        # perhaps store mult funcs in a lits and iterate over them
        
        # Alteration multiplier
        self.multiplier *= self.get_alteration_mult()
        
        self.av = int(self.value * self.multiplier)
    
    
    def get_alteration_mult(self):
        '''
        Applies highest potency buff and debuff to stat mult
        '''

        # Prevent index out of bounds, Get values if they exist
        buff_val = 1 if self.buffs == [] else self.buffs[0].value
        debuff_val = 1 if self.debuffs == [] else self.debuffs[0].value
        
        # TODO: incorporate Hunger apt mult here
        return buff_val * debuff_val
    
    ''' 
                            PERM CHANGE FUNCS
    ''' 
    def change_base_value(self, amount:int):
        
        # Reduce shrink by positive aptitude multipliers
        if amount < 0 and self.apt > 0:
            amount /= get_mult_of_aptitude(self.apt)
        
        # cap lowest value to 1
        change = self.value + amount if self.value + amount > 1 else 1
        
        self.set_new_vals(change, self.apt)
        
    def change_aptitude_xp(self, amount:int):
        self.apt_exp += amount
        
        #cap
        if self.apt_exp < 0:
            self.apt_exp = 0
          
        elif self.apt_exp > XP_REQURED_PER_APT[8]:
            self.apt_exp = XP_REQURED_PER_APT[8]

        
        #get apt with the exp value that is less than, yet closest to the current exp
        for apt, req_xp in XP_REQURED_PER_APT.items():
            if self.apt_exp >= req_xp:
                self.apt = apt
            else:
                break
        
        self.set_new_vals(self.value, self.apt)
         

''' 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        GENERIC FUNCTIONS, EQUATIONS & CONSTANTS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
  
STAT_TYPES = {
        "strength": Stat("strength", 0, 0, "str", ["s", "fuerza"]),
        "defense": Stat("defense", 0, 0, "def", ["d", "defensa"]),
        "evasion": Stat("evasion", 0, 0, "eva", ["e", "evade"]),
        "dexterity": Stat("dexterity", 0, 0, "dex", ["dx", "destreza"]),
        "recovery": Stat("recovery", 0, 0, "rec", ["r", "recuperación"]),
        "intelligence": Stat("intelligence", 0, 0, "int", ["i", "intellect", "inteligencia"]),
        "creativity": Stat("creativity", 0, 0, "cre", ["c", "create", "creatividad"]),
        "fear": Stat("fear", 0, 0, "fear", ["f", "spook", "miedo"]),
        "intimidation": Stat("intimidation", 0, 0, "itmd", ["it", "intim","intimidacion"]),
        "charisma": Stat("charisma", 0, 0, "cha", ["ch", "char", "carisma"]),
        "stress": Stat("stress", 0, 0, "tres", ["ss", "estres"]),
        "health": Stat("health", 0, 0, "hp", ["h", "health points", "salud", "puntos de salud"]),
        "hunger": Stat("hunger", 0, 0, "hun", ["hu", "hung", "hambre"]),
        "energy": Stat("energy", 0, 0, "ap", ["a", "action points", "energia", "puntos de accion"]),
}

def convert_base_number_to_multiplier(number:int, base_stat:int):
    return number / base_stat + 1

def reduce_decreasing_modifier(apt_mult:float, modifier:float):
    '''
    When a stat has a decreasing modifier (debuff), it should be reduced based on the increasing
    aptitude multiplier of the stat.
    This function calculates the new modifier by multiplying 1 divided by aptitude multiplier with
    the inverse of the modifier multiplier and then taking one to subtract by the product
    
    Example:
        With an aptitude of 4 and a multiplier of 0.9,
        the multiplier will have its effect halved by converting it into 0.95.

    Parameters:
        apt_mult (float): Aptitude multiplier of the stat
        modifier (float): Modifier multiplier to be reduced

    Returns:
        float: Reduced modifier
    '''
    if apt_mult < 1:
        raise ValueError("Aptitude multiplier must be greater than 1, an increasing multiplier")
    
    if modifier > 1:
        raise ValueError("Modifier must be less than 1, a decreasing modifier")
    
    a = 1 / apt_mult
    m = 1 - modifier
    return 1 - (m * a)

def reduce_increasing_modifier(apt_mult:float, modifier:float):
    '''
    When a stat has an increasing modifier (buff), it should be reduced based on the decreasing 
    aptitude multiplier of the stat.
    This function calculates the new modifier by multiplying the inverse of the modifier 
    by the aptitude multiplier and then adding one

    Example:
        With an aptitude of -4 and a multiplier of 1.1,
        the multiplier will have its effect halved by converting it into 1.05.
    
    Parameters:
        apt_mult (float): Aptitude multiplier of the stat
        modifier (float): Modifier multiplier to be reduced

    Returns:
        float: Reduced modifier
    '''
    if apt_mult > 1:
        raise ValueError("Aptitude multiplier must be less than 1, a decreasing multiplier")
    
    if modifier < 1:
        raise ValueError("Modifier must be greater than 1, an increasing modifier")
    
    return 1 + ((1 - modifier) * apt_mult)
        

def sn(name):
    """
    Returns the full name of a stat given a name, abreviation, or 
    any of the extra applicable names. Case insensitive. 
    Raises NameError if stat name not found.

    Parameters:
        name (str): name of stat

    Returns:
        str: full name of stat
    """
    for stat in STAT_TYPES.values():
        poss_names = stat.get_all_names()
        if name.lower() in poss_names:
            return stat.name
    
    raise NameError(f"The string {name} could not be matched to a valid stat name")
            
            
def make_stat(name, val, apt):
        name = sn(name).lower()
        stat = copy.deepcopy(STAT_TYPES[name])
        stat.apt = apt
        stat.value = val
        stat.apt_exp = XP_REQURED_PER_APT[stat.apt]
        stat.calc_active_value()
        return stat

''' 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                        STAT BOARD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

class StatBoard:
    
    def __init__(self, stats_dict: dict):
        self.cur_stats = stats_dict
        # These stats dont ever have Alterations applied to them
        # and are only affected by permanent upgrades/effects
        self.mem_stats = stats_dict
        
    def get_stat(self, name):
        for s in self.cur_stats.values():
            if s.name == sn(name):
                return s
        return None
    
    def set_cur_stat_to_mem_stat(self, name):
        for s in self.cur_stats.values():
            if s.name == sn(name):
                self.cur_stats[s.name].val = self.mem_stats[s.name].val
                self.cur_stats[s.name].apt = self.mem_stats[s.name].apt
            
    def get_stat_apts(self):
        return {stat.name: stat.apt for stat in self.cur_stats.values()}
    
    def get_stat_avs(self):
        return {stat.name: stat.av for stat in self.cur_stats.values()}
     
    def initiative(self):
        return self.cur_stats["dexterity"].av + self.cur_stats["evasion"].av
    
    def apply_init_ap_bonus(self):
        self.apply_alteration(ap_buff)

    def apply_alteration(self, alt: Alteration):
        
        # obtain correct list to apply alteration
        stat_name = sn(alt.ef_stat)
        alt_list = (self.cur_stats[stat_name].buffs 
                    if alt.is_buff 
                    else self.cur_stats[stat_name].debuffs)
        
        # call alteration apply func
        # trigger recalc of stat value if True is returned
        recalc = alt.apply(alt_list)
        
        if recalc:
            self.cur_stats[stat_name].calc_active_value()
        
    def remove_alteration(self, alteration: Alteration):
        for s in self.cur_stats.values():
            if s.name == sn(alteration.ef_stat):
                if alteration.value > 1:
                    s.buffs.remove(alteration)
                else:
                    s.debuffs.remove(alteration)
                break
            
    # TEMPORARY func to tick alterations.
    def tick_alterations(self):
        for s in self.cur_stats.values():
            for b in s.buffs:
                if b.tick():
                    print("Removed buff: " + b.name)
                    s.buffs.remove(b)   
            for d in s.debuffs:
                if d.tick():
                    print("Removed debuff: " + d.name)
                    s.debuffs.remove(d)
      
       
                    
    def get_all_buffs(self):
        all_buffs = {}
        for s in self.cur_stats.values():
            all_buffs[s.name] = s.buffs
        return all_buffs
    
    def get_all_debuffs(self):
        all_debuffs = {}
        for s in self.cur_stats.values():
            all_debuffs[s.name] = s.debuffs
        return all_debuffs
        
 
'''
                                  DEPOSED FOR NOW

def get_xp_to_level(apt:int):
    
    #exit condition
    if apt == -4:
        return 0
    
    MAX_POINTS = 40
    MAX_DIVISOR = 10
    divisor = 1
    
    # inverted absolute value graph with a steeper left slope
    # top point, where x=0 is the max divisor of the max points
    # https://www.desmos.com/calculator/fszon1uzau
    if apt >= 0:
        divisor = -1.125 * abs(apt) + MAX_DIVISOR
    elif apt < 0:
        divisor = -2.25 * abs(apt) + MAX_DIVISOR
    
    # prevent division by zero
    divisor = 1 if divisor == 0 else divisor
    
    return math.floor(MAX_POINTS / divisor + 0.5) + get_xp_to_level(apt - 1)  

def store_points_req_per_level():
    for apt in range(-4, 9):
        XP_REQURED_PER_APT[apt] = get_xp_to_level(apt)
'''