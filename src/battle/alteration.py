import enum
from enum import auto

class Alteration:

    class Grade(enum.Enum):
        LESSER = auto()
        MINOR = auto()
        MAJOR = auto()
        GREAT = auto()
        ULTIMATE = auto()
        BEWILDERING = auto()
    
    def __init__(self, name: str, value: float, duration: int, ef_stat: str):
        
        if value < 0 or value == 1:
            raise Exception("Alteration value must be greater than or equal to 0 and cannot be 1")
        
        self.name = name # won't be displayed in game, only used for internal equality checks
        self.value = value
        self.is_buff = value > 1
        self.duration = duration #TODO: will be changed into its own object
        self.duration_left = duration
        self.ef_stat = ef_stat
        
    def __eq__(self, other):
        if isinstance(other, Alteration):
            return (self.name == other.name or (self.value == other.value 
                    and self.duration == other.duration and self.ef_stat == other.ef_stat ))
        return NotImplemented
    
    def __str__(self):
        return f"{self.name}: ({round(self.value, 3)}) | {self.duration_left} turns left"
    
    def get_grades():
        return [grade for grade in Alteration.Grade]
    
    def tick(self):
        self.duration_left -= 1
        return self.duration_left <= 0
        
    def is_this_more_potent(self, alt):
        if not isinstance(alt, Alteration) or self.is_buff != alt.is_buff:
            return None
        
        if self.is_buff:
            return self.value > alt.value
        else:
            return self.value <= alt.value
        
    def apply(self, alt_list:list):
        '''
        Applies this alteration to the list of alterations, assuming
        the list is sorted by potency then duration, the list only regards one stat,
        and the list is populated with Alterations of the same value type as this one
        (buffs or debuffs)
        
        Returns:
            bool: if this alteration has the highest potency and the stat value should be recalculated
        '''
        
        if alt_list == []:
            alt_list.append(self)
            return True
        
        for i, a in enumerate(alt_list):
            
            # This alteration is more potent, insert it in front of this index
            if self.is_this_more_potent(a):
                alt_list.insert(i, self)
                return i == 0 
            
            # If the potency is the same, perhaps this alteration is a copy or will 
            # increase duration left
            # TODO: allow for different duration types and comparisons, like a move versus a day
            # TODO: alert game if alteration was refreshed or extended
            # current funcctionality is ONLY turn based
            if self.value == a.value:
                # refresh duration
                if self.duration == a.duration or self.duration > a.duration:
                    a.duration_left = (self.duration 
                                       if a.duration_left < self.duration 
                                       else a.duration_left)
                    # EDGE CASE: 
                        # refresh is ignored if it would actually reduce the duration left
                    return False
             
            # This alteration is the least potent, add it to the end
            if not self.is_this_more_potent(a) and i == len(alt_list) - 1:
                alt_list.append(self)
                return False

AP_BUFF = Alteration("Intiative Bonus", 1.5, 1, "AP")

def create_alteration(effected_stat_name:str, mult:float, duration:int) -> Alteration:
    
    name = ''
    if mult < 1:
        name = "-" + str((1 - mult) * 100) + "%"
    else:
        name = "+" + str((mult-1) * 100) + "%"
    
    return Alteration(name=f"{name} {effected_stat_name}", value=mult, 
                      duration=duration, ef_stat=effected_stat_name)

def get_grade_values(grade:Alteration.Grade, values_out:dict[str,int]):
    
    if(grade == Alteration.Grade.LESSER):
        values_out['mult'] = 1.1
        values_out['duration'] = 6
    elif(grade == Alteration.Grade.MINOR):
        values_out['mult'] = 1.2
        values_out['duration'] = 5
    elif(grade == Alteration.Grade.MAJOR):
        values_out['mult'] = 1.5
        values_out['duration'] = 3
    elif(grade == Alteration.Grade.GREAT):
        values_out['mult'] = 2
        values_out['duration'] = 2
    elif(grade == Alteration.Grade.ULTIMATE):
        values_out['mult'] = 3
        values_out['duration'] = 1
    elif(grade == Alteration.Grade.BEWILDERING):
        values_out['mult'] = 10
        values_out['duration'] = 1

def get_grade_info_as_str_lst():
    lst = []
    value = {'mult': 0, 'duration': 0}
    
    for grade in Alteration.Grade:
        get_grade_values(grade, value)
        lst.append((f"{grade.name:<11} -  mult val: {round(value['mult'], 3):<3}" 
                    + f" | duration: {value['duration']:<3}"
                    ))
    return lst

def create_preset_alt(effected_stat_name:str, is_buff:bool, grade:Alteration.Grade) -> Alteration:

    value = {'mult': 0, 'duration': 0}
    
    get_grade_values(grade, value)
    
    suffix = ""
       
    if not is_buff:
        value['mult'] = 1/value['mult']
        suffix = "debuff"
    else:
        suffix = "buff"
    
    return Alteration(name=f"{grade.name} {effected_stat_name} {suffix}", 
                      value=value['mult'], duration=value['duration'], 
                      ef_stat=effected_stat_name)
