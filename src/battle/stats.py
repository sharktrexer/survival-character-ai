import copy

from battle.alteration import Alteration, AP_BUFF
#from battle.multipliers import MultChange

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
        self.val_resource = val
        self.apt = apt
        self.apt_exp = 0 
        self.val_active = 0
        self.multiplier = 1.0
        '''separate mult modifier that is effected by everything else 
        other than aptitude and alterations'''
        self.ex_mults = 1.0 
        
        # Alterations 
        self.buffs: list[Alteration] = []
        self.debuffs: list[Alteration] = []
        
        
        #TODO: should this class have a way to point to its battlepeep owner?
     
    def __eq__(self, other):
        if isinstance(other, Stat):
            return self.name == other.name and self.apt == other.apt and self.value == other.value
        return False
        
    def __str__(self):
        return (f"{self.name.upper()}: \nApt - {self.apt:<3} Val - {self.value:<4} Active Val - {self.val_active:<4}" 
                + f"\nCurrent Modifier - {round(self.multiplier, 3):<4}"
                + f"\nCurrent Apt Exp - {self.apt_exp:<4} Exp to Next Level - {self.get_xp_req_to_next_apt_level():<4}")
    
    ''' 
                                HELPER FUNCTIONS
    ''' 
    def simple_str(self):
        return f"{self.name.upper()}: \nApt - {self.apt:<3} Val - {self.value:<4} Active Val - {self.val_active:<4}" 
    
    def get_all_names(self):
        return [self.name, self.name.lower(), self.abreviation] + self.ex_names
    
    def get_xp_req_to_next_apt_level(self):
        if self.apt == 8: return 0
        
        return XP_REQURED_PER_APT[self.apt + 1] - self.apt_exp
    
    def get_all_alterations(self) -> list[Alteration]:
        ''' returns the list of buffs + debuffs'''
        return self.buffs + self.debuffs
    
    def get_buff_info_as_str(self):
        buff_info = "\nBuffs:\n"
        for buff in self.buffs:
            buff_info += "\t" + str(buff) + "\n"
        return buff_info
    
    def get_debuff_info_as_str(self):
        debuff_info = "\nDebuffs:\n"
        for debuff in self.debuffs:
            debuff_info += "\t" + str(debuff) + "\n"
        return debuff_info
    
    def get_alt_info_as_str(self):
        alt_info = self.get_buff_info_as_str()
            
        alt_info += self.get_debuff_info_as_str()
        
        return alt_info
    
    def get_debuff_mult(self):
        # Prevent index out of bounds, Get values if they exist
        return 1 if self.debuffs == [] else self.debuffs[0].value
    
    def get_buff_mult(self):
        # Prevent index out of bounds, Get values if they exist
        return 1 if self.buffs == [] else self.buffs[0].value
    
    #TODO: perhaps all the string funcs can be placed into peep_manager?
    def get_active_alt_info_as_str(self):
        buff = self.get_buff_mult()
        debuff = self.get_debuff_mult()
        return ("Buff Mult: " + str(round(self.get_buff_mult(), 3)) 
                + "\nDebuff Mult: " + str(round(self.get_debuff_mult(), 3))
                + "\nFinal Mult: " + str(round(buff * debuff, 3)))
    
    ''' 
                            ACTIVE VALUE CALCULATION
    '''
    def set_new_vals(self, val:int, apt:int):
        self.value = int(val)
        self.apt = int(apt)
        self.calc_active_value()
        
    def set_new_vals_as_reset(self, val:int, apt:int):
        """
        Resets a stat to a new value and aptitude, resetting the resource value,
        deleting all buffs, debuffs, extra mults, and setting the apt exp to the exp amount
        of the corresponding aptitude level. 
        """
        
        self.buffs = []
        self.debuffs = []
        self.ex_mults = 1.0
        self.set_new_vals(val, apt)
        self.apt_exp = XP_REQURED_PER_APT[self.apt]
        self.val_resource = self.val_active
        
    def set_new_vals_as_update(self, val:int, apt:int, apt_exp:int):
        self.set_new_vals(val, apt)
        self.apt_exp = apt_exp
        
    def set_extra_mult(self, mult:float):
        '''
        Sets the extra multiplier of the stat
        and recalcs the active value
        '''
        self.ex_mults = mult
        self.calc_active_value()
        
    def calc_active_value(self):
        # reset
        self.multiplier = 1
        
        # add apt multiplier
        self.multiplier *= get_mult_of_aptitude(self.apt)
        
        # ADD OTHER MULTIPLIERS HERE
        # perhaps store mult funcs in a list and iterate over them
        self.multiplier *= self.ex_mults
        
        # Alteration multiplier
        self.multiplier *= self.get_alteration_mult()
        
        final_val = int(self.value * self.multiplier)
        
        # active value can't be less than 1
        self.val_active = final_val if final_val > 1 else 1
    
    def get_alteration_mult(self):
        '''
        Returns the combined mult of the highest potency buff and debuff
        ''' 
        buff_val = self.get_buff_mult()
        debuff_val = self.get_debuff_mult()
        
        # TODO: incorporate Hunger apt mult here
        return buff_val * debuff_val
    
    def remove_all_alterations(self):
        self.buffs = []
        self.debuffs = []
        self.calc_active_value()
        
    def remove_alteration(self, alt_ind:int):
        '''
        Removes the alteration at the given index from the stat.
        Index is assumed to be the index of the list "buffs + debuffs"
        '''
        if alt_ind < len(self.buffs):
            self.buffs.pop(alt_ind)
        else:
            self.debuffs.pop(alt_ind - len(self.buffs))
        
        # recalc active value if the highest priority buff or debuff was removed
        # (at index 0 of either buffs or debuffs)
        if alt_ind == 0 or alt_ind == len(self.buffs) :    
            self.calc_active_value()
    
    ''' 
                            RESOURCE VALUE FUNCS
    '''
    def resource_restore(self):
        self.resource_set_to_percent(1.0)
        
    def resource_change(self, amount:int) -> bool:
        '''
        Adds the given amount to the resource value of this stat
        Resource value cannot be depleted to less than 0 
        or increased beyond the active value
        
        Returns:
            if the resource of this stat has been depleted
        '''
        
        self.val_resource += amount
        
        # cap
        if self.val_resource > self.val_active:
            self.val_resource = self.val_active
        elif self.val_resource <= 0:
            self.val_resource = 0
            return True
        return False
    
    def resource_set_to_percent(self, percent:float):
        self.val_resource = int(self.val_active * percent)
    
    
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
                        GENERIC FUNCTIONS, CLASSES, EQUATIONS & CONSTANTS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

class StatChange():
    '''
    Simple class to represent a permanent stat change
    '''
    def __init__(self, stat_name:str, val_amount:int, apt_xp_amount:int):
        self.name = sn(stat_name)
        self.val_amount = val_amount
        self.apt_xp_amount = apt_xp_amount
        
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

def convert_whole_number_to_multiplier(whole_num:int, affected_number:int) -> float:
    '''
    Converts a whole positive or negative number to a multiplier to apply to the affected number
    
    Example:
        With a whole number of 5 and an affected number of 10,
        the multiplier will be 1.5
    
    Returns:
        float: The multiplier
    '''
    return whole_num / affected_number + 1

def convert_muliplier_to_whole_number(multiplier:float, affected_number:int) -> int:
    '''
    Converts a multiplier into a positive or negative number to be added to the affected number
    
    Example:
        With a multiplier of 1.5 and an affected number of 10,
        the whole number will be 5
    
    Returns:
        int: The whole number
    '''    
    return affected_number * multiplier - affected_number

def reduce_decreasing_modifier(apt:int, modifier:float):
    '''
    When a stat has a decreasing modifier (debuff), it should be reduced 
    based on the increasing aptitude multiplier of the stat.
    
    Get inverse of aptitude increasing multiplier
    Get the difference between 1 and the decreasing modifier
    Multiply the inverse by the difference 
    Get the difference of 1 from the product
    
    
    Example:
        With an aptitude of 4 and a multiplier of 0.9,
        the multiplier will have its effect halved by converting it into 0.95.

    Parameters:
        apt_mult (float): Aptitude multiplier of the stat
        modifier (float): Modifier multiplier to be reduced

    Returns:
        float: Reduced modifier
    '''
    apt_mult = get_mult_of_aptitude(apt)
    
    if apt_mult < 1:
        raise ValueError("Aptitude multiplier must be greater than 1, an increasing multiplier")
    
    if modifier > 1:
        raise ValueError("Modifier must be less than 1, a decreasing modifier")
    
    a = 1 / apt_mult
    m = 1 - modifier
    return 1 - (m * a)

def reduce_increasing_modifier(apt:int, modifier:float):
    '''
    When a stat has an increasing modifier (buff), it should be reduced based on the decreasing 
    aptitude multiplier of the stat.
    
    Get difference of positive modifier from 1
    Multiply by reducing aptitude multiplier
    Add 1 to the product

    Example:
        With an aptitude of -4 and a multiplier of 1.1,
        the multiplier will have its effect halved by converting it into 1.05.
    
    Parameters:
        apt_mult (float): Aptitude multiplier of the stat
        modifier (float): Modifier multiplier to be reduced

    Returns:
        float: Reduced modifier
    '''
    apt_mult = get_mult_of_aptitude(apt)
    
    if apt_mult > 1:
        raise ValueError("Aptitude multiplier must be less than 1, a decreasing multiplier")
    
    if modifier < 1:
        raise ValueError("Modifier must be greater than 1, an increasing modifier")
    
    return ((modifier - 1) * apt_mult) + 1
        

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
    '''
    Creates a stat object from a name, value, and aptitude
    '''
    name = sn(name).lower()
    stat = copy.deepcopy(STAT_TYPES[name])
    stat.apt = apt
    stat.value = val
    stat.apt_exp = XP_REQURED_PER_APT[stat.apt]
    stat.calc_active_value()
    stat.val_resource = stat.val_active
    return stat

def divide_resource_max_by(stat:Stat, divisor:int):
    if divisor < 1:
        return 0
    return round(stat.val_active / divisor, 2)

''' 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                        STAT BOARD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

class StatBoard:
    
    def __init__(self, stats_dict: dict[str, Stat]):
        self.cur_stats = stats_dict
        # These stats dont ever have Alterations applied to them
        # and are only affected by permanent upgrades/effects
        self.mem_stats = stats_dict
        
        # list of mult changes to apply to stats. 
        # one entry equals the total mult change of one stat
        # default mult change for every stat is 1
        '''self.mult_changes = dict(zip(STAT_TYPES.keys(), 
                                     [MultChange(name, 1) for name in STAT_TYPES.keys()]
                                    )
                                )'''
        
    def get_stat_cur(self, name):
        return self.cur_stats[sn(name)]
    
    def get_stat_mem(self, name):
        return self.mem_stats[sn(name)]
    
    def get_stat_active(self, name):
        return self.cur_stats[sn(name)].val_active
    
    def get_stat_resource(self, name):
        return self.cur_stats[sn(name)].val_resource
    

    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MANIPULATING PERM & CUR STATS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    '''
    
    def set_cur_stat_to_mem_stat(self, mem_stat:Stat):
        name = mem_stat.name
        self.cur_stats[name].set_new_vals_as_update(mem_stat.value, mem_stat.apt, mem_stat.apt_exp)
        
    def change_apt_xp(self, stat_name:str, xp:int):
        stat = self.get_stat_mem(stat_name)
        stat.change_apt_xp(xp)
        stat.set_cur_stat_to_mem_stat(stat.name)
    
    def change_stat_base_val(self, stat_name:str, amount:int):
        stat = self.get_stat_mem(stat_name)
        stat.change_base_val(amount)
        self.set_cur_stat_to_mem_stat(stat.name)
        
    def mults_apply(self):
        '''
        Call to apply all multiplier changes to stats
        '''
        total_mult = 1
        for change in self.mult_changes:
            total_mult *= change.mult
            
        self.get_stat_cur(change.stat_name).set_extra_mult(total_mult)    
    def mults_reset(self):
        for change in self.mult_changes:
            change.mult = 1
        self.mults_apply()
    
    '''
        Reserved for stats like Hunger, Energy, Health, Stress, & Fear
    '''   
    def resource_change(self, stat_name, amount):
        '''
        Adds the passed in amount to the passed in stat's resource value
        
        Returns:
            if the resource of the current stat is depleted
        '''
        return self.cur_stats[sn(stat_name)].resource_change(amount)
    
    def resource_restore(self, stat_name):
        '''
        Restores the passed in stat's resource value to its max value (active value)
        '''
        self.cur_stats[sn(stat_name)].resource_restore()
        
    def resource_is_depleted(self, stat_name):
        '''
        Returns:
            if the resource of the current stat is depleted (0)
        '''
        return self.cur_stats[sn(stat_name)].val_resource <= 0
    
    def resource_set_to_percent(self, stat_name:str, percent:float):
        
        # caps
        if percent < 0:
            percent = 0   
        elif percent > 1:
            percent = 1
        
        self.cur_stats[sn(stat_name)].resource_set_to_percent(percent)
 
#TODO: these should be in a higher level class. Statboard doesn't need to know about sleeping
    def calc_hrs_req_to_sleep(self):
        if self.cur_stats["energy"].apt >= 0:
            return 8
        else:
            return 8 + abs(self.cur_stats["energy"].apt)
    
    def sleep_by_min(self):
        #TODO: affect stress, fear, and hunger
        
        health_stat = self.cur_stats[health_stat]
        amnt_per_min = divide_resource_max_by (health_stat, self.calc_hrs_req_to_sleep() * 60)
        health_stat.resource_change(amnt_per_min)
        
        '''
        Time Spent Asleep:
        With 0 Energy Aptitude or Higher: 
            peeps need 8 hours of sleep.
        Per point of Energy Apt below 0: 
            peeps need +1 more hrs of sleep (12 max)'''
        
    
    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EXTRA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    '''
            
    def get_all_stat_apts(self):
        return {stat.name: stat.apt for stat in self.cur_stats.values()}
    
    def get_all_stat_active_value(self):
        return {stat.name: stat.val_active for stat in self.cur_stats.values()}
     
    def initiative(self):
        '''
        Combined active values of Dexterity and Evasion
        '''
        return self.cur_stats["dexterity"].val_active + self.cur_stats["evasion"].val_active
    
    def get_all_stats_as_str(self):
        stats_2_str = ""
        for stat in self.cur_stats.values():
            stats_2_str += str(stat) + "\n---------------------------\n"
        return stats_2_str
    
    def get_all_alts_as_str(self):
        '''
        Returns a formatted string of all alterations on every stat
        
        EXAMPLE:
            stat_name: alteration_mult
            alt_name: (mult_val) | (duration)
            etc...
        '''
        
        alts_2_str = ""
        
        for stat in self.cur_stats.values():
            alts_2_str += "----------------------------\n" + stat.name.upper() + ": "
            alts_2_str += str(round(stat.get_alteration_mult(), 2)) + "\n"
            for alt in stat.get_all_alterations():
                alts_2_str += str(alt) + "\n"
                
        return alts_2_str
    
    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ALTERATIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    '''
    
    def apply_init_ap_bonus(self):
        self.apply_alteration(AP_BUFF)

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
     
    #TODO: needs rewrite?   
    def remove_alteration(self, alteration: Alteration):
        for s in self.cur_stats.values():
            if s.name == sn(alteration.ef_stat):
                if alteration.value > 1:
                    s.buffs.remove(alteration)
                else:
                    s.debuffs.remove(alteration)
                break
            
    def remove_all_alterations(self):
        for s in self.cur_stats.values():
            s.remove_all_alterations()
            
    # func to tick alterations while alterations only rely on turns
    def tick_alterations(self):
        for s in self.cur_stats.values():
            for i, alt in enumerate(s.get_all_alterations()):
                if alt.tick():
                    s.remove_alteration(i)
      
    def get_all_alterations(self) -> list[Alteration]:
        all_alts = []
        for s in self.cur_stats.values():
            for alt in s.get_all_alterations():
                all_alts.append(alt)
        return all_alts
                    
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