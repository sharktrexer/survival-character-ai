from character import Character

# List of all the stat names used by characters
STAT_NAMES = [
        "Strength", "Defense", "Evasion",   
                
        "Dexterity", "Recovery", "Intellect", 
        
        "Creativity", "Fear", "Intimidation",
        
        "Charisma", "Stress", "Health", 
        
        "Hunger", "Energy", 
    ]

def make_peep(name, desc, stat_vals):
    '''Easily creates characters while verifying they have the right amount of stat distribution'''
    val_total = sum(stat_vals)
    
    if (val_total != 18 or (name == "Rebecca" and val_total != 0)):
        raise Exception(f"Character \"{name}\" does not have a total of 18 points in their stats, but instead {val_total}")
    
    return Character(name, desc, dict(zip(STAT_NAMES, stat_vals)))

''' 
List of preset characters

Combines stat name list with numerical values to create and
store dictionary of customized stats with associated names
'''
PEOPLE = [
    make_peep("Chris", 
              "Perfectionist", [4,3,-2,1,-1,2,5,0,1,1,-2,4,-1,3]),
    
    make_peep("Adan", 
              "Handsome Rogue", [0,2,5,4,2,1,1,1,-2,2,1,0,0,1]),
]

def print_peeps():
    for p in PEOPLE:
        print(p, "\n")
        
print_peeps()