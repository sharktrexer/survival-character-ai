import os, csv

from battle.battle_peep import BattlePeep
from peep_data.character import Character
from battle.stats import STAT_TYPES, make_stat

STAT_PATH = os.getcwd() + "\\src\\peep_data\\char_data.csv"
DESC_PATH = os.getcwd() + "\\src\\peep_data\\char_desc.csv"
MAGIC_PATH = os.getcwd() + "\\src\\peep_data\\char_magic.csv"

# Max amount of points that can be distributed amongst character stats
MAX_STAT_VAL = 18

# holds the default stats of the OG characters
PEEPS = []
TITLES = []
DESCS = []
SIMPLE_PEEPS = []

'''
--------------------------------------------- CSV READS ---------------------------------------------
'''

def read_peep_stat_data():
    with open(STAT_PATH, 'r') as file:   
        reader = csv.DictReader(file)
        # Every row is a character with name and stats
        for char_stats_dict in reader:
            stats_dict = {}
            
            # loop thru key/val parts (stat name and apt)
            # column after the stat's aptitude is its value
            s_name = ""
            s_apt = ""
            for key, val in char_stats_dict.items(): 
                
                key = key.lower()
                
                # Name already obtained
                if key == "name": continue
                # Obtain aptitude value
                if key in STAT_TYPES.keys():
                    s_name = key
                    s_apt = val
                # If key isn't a stat name then assume the val is the stat's numerical value
                # STAT obj can be created with both apt and val
                else:
                    stats_dict[s_name] = make_stat(s_name, int(val), int(s_apt)) 
                    # reset vals for easier debugging
                    s_name = ""
                    s_apt = ""
                
                    
            PEEPS.append(BattlePeep(char_stats_dict["name"], stats_dict))
 
 
def read_peep_desc_data():
    with open(DESC_PATH, 'r') as file:   
        reader = csv.DictReader(file)
        # Every row is a char name, title, and describing sentence
        for row in reader:
            TITLES.append(row["Title"])
            DESCS.append(row["Personality"]) 
            

def read_peep_magic_data():
    with open(MAGIC_PATH, 'r') as file:   
        reader = csv.DictReader(file)
        # Every row is a char name, primary, secondary, tertiary magic name
        for row in reader:
            # calc stat resistances and add to peeps
            pass

'''
--------------------------------------------- SIMPLE PEEPS ---------------------------------------------
'''

def check_peep(peep: Character):
    '''Verifies characters have the right amount of stat distribution'''
    val_total = sum(peep.get_stat_apts().values())
    
    # Rebecca has a special case
    val_total = MAX_STAT_VAL if peep.name == "Rebecca" and val_total == 0 else val_total
    
    if val_total != MAX_STAT_VAL:
        raise Exception(f"Character \"{peep.name}\" does not have a total of {MAX_STAT_VAL} points in their stats, but instead {val_total}")
            
def create_simple_peeps():
    """
    Creates a list of Character objects from BattlePeep objects with simpler info.
    """
    for i, bp in enumerate(PEEPS):
        check_peep(bp)
        SIMPLE_PEEPS.append(Character(bp.name, TITLES[i], DESCS[i], 
                                bp.get_stat_apts()))
            
read_peep_stat_data()
read_peep_desc_data()
read_peep_magic_data()

create_simple_peeps()