import os, csv

from battle.battle_peep import BattlePeep
from battle.stats import STAT_TYPES, make_stat

PATH = os.getcwd() + "\\src\\peep_data\\char_data.csv"

# holds the default stats of the OG characters
PEEPS = []

def get_peeps(): 
    return PEEPS

def read_peep_data():
    with open(PATH, 'r') as file:   
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
            