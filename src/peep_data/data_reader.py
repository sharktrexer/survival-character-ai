import os, csv
from battle.battle_peep import BattlePeep
from battle.stats import Stat

PATH = os.getcwd() + "\\src\\peep_data\\char_data.csv"

STAT_NAMES = [
        "Strength", "Defense", "Evasion",   
                
        "Dexterity", "Recovery", "Intelligence", 
        
        "Creativity", "Fear", "Intimidation",
        
        "Charisma", "Stress", "Health", 
        
        "Hunger", "Energy", 
    ]

# holds the default stats of the OG characters
PEEPS = []

def get_peeps(): return PEEPS

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
                # Name already obtained
                if key == "name": continue
                # Obtain aptitude value
                if key in STAT_NAMES:
                    s_name = key
                    s_apt = val
                # If key isn't a stat name then assume the val is the stat's numerical value
                # STAT obj can be created with both apt and val
                else:
                    stats_dict[s_name] = Stat(s_name, int(val), int(s_apt))
                    s_name = ""
                    s_apt = ""
                
                    
            PEEPS.append(BattlePeep(char_stats_dict["name"], stats_dict))