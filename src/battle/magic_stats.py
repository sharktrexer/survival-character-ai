from enum import Enum

'''
All magic damage pulls from INT + MagicStat

Then some may apply another stat:
    fire - 
    ice - 
    water - Rec 
    earth - 
    holy - 
    psychic - Cha 
    shadow - Itmd 
    lightning - 
    mundane - 
    wind - 
'''

COUNTER_MAGIC_MULTS = [0.5, 0.25, 0.1]
SAME_MAGIC_MULTS = [0.25, 0.1, 0.05]
# magic of the same type will have half of much resistance as counters

class MagicStat:
    def __init__(self, name:str, resistance:float, priority:int):
        self.name = name
        self.resistance = resistance
        self.priority = priority
        
class MagicBoard:
    def __init__(self, magic_aptitudes:dict[str, int]):
        '''
        Parameters:
            starting_magics (dict[str, int]): magic name, priority
        '''
        self.magics:dict[str, MagicStat] = {}
        

MAGIC_NAMES = [
    'fire',
    'ice',
    'water',
    'earth',
    'holy',
    'psychic',
    'shadow',
    'lightning',
    'mundane',
    'wind'
    ]

def get_magics_vul_and_countered_relation(magic_name:str):
    this_index = MAGIC_NAMES.index(magic_name)
    
    vuln_index = (this_index - 1) % len(MAGIC_NAMES)
    vuln_name = MAGIC_NAMES[vuln_index]
    
    countered_index = (this_index + 1) % len(MAGIC_NAMES)
    countered_name = MAGIC_NAMES[countered_index]
    
    return (vuln_name, countered_name)

def get_res_value(priority:int, magic_name:str):
    '''
    
    Returns:
        dict[str, float] = magic_name, resist multiplier
        
        Where names are in the following order
        
        1. magic I am vulnerable to (previous MAGIC_NAMES element), 
        
        2. my same type, 
        
        3. magic that I counter (next MAGIC_NAMES element)
    '''
    
    if priority > 3 or priority < 1:
        raise ValueError(('Priority must be between 1 and 3,' 
                          'representing primary, secondary, and tertiary'))
    
    priority -= 1 # convert into 0 index
    
    vuln_mag, countered_mag = get_magics_vul_and_countered_relation(magic_name)
    
    return {vuln_mag: -COUNTER_MAGIC_MULTS[priority], 
            magic_name: SAME_MAGIC_MULTS[priority],
            countered_mag: COUNTER_MAGIC_MULTS[priority]}
    
#TODO: func to get and store all magic resists from a character's 3 different magics
    
