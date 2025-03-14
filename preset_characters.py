from character import Character

# List of all the stat names used by characters
STAT_NAMES = [
        "Strength", "Defense", "Evasion",   
                
        "Dexterity", "Recovery", "Intellect", 
        
        "Creativity", "Fear", "Intimidation",
        
        "Charisma", "Stress", "Health", 
        
        "Hunger", "Energy", 
    ]

# Max amount of points that can be distirbuted amognst character stats
MAX_STAT_VAL = 18

def make_peep(name: str, desc: str, stats: dict):
    '''Easily creates characters while verifying they have the right amount of stat distribution'''
    val_total = sum(stats.values())
    
    # Rebecca has a special case
    val_total = MAX_STAT_VAL if name == "Rebecca" and val_total == 0 else val_total
    
    if val_total != MAX_STAT_VAL:
        raise Exception(f"Character \"{name}\" does not have a total of {MAX_STAT_VAL} points in their stats, but instead {val_total}")
    
    return Character(name, desc, stats)

''' 
List of preset characters

Combines stat name list with numerical values to create and
store dictionary of customized stats with associated names
'''
PEOPLE = [
    make_peep("Chris", 
              "Reactive Chef", 
              {
                "Strength": 4, "Defense": 4, "Evasion":-2,
                "Dexterity": 0, "Recovery": -1, "Intellect": 3,
                "Creativity": 5, "Fear": 2, "Intimidation": 2,
                "Charisma": 2, "Stress": -4, "Health":3,
                "Hunger": -1, "Energy": 1
                }),
    
    make_peep("Adan", 
              "Cunning Rogue", 
              {
                "Strength": 1, "Defense": 2, "Evasion": 5,
                "Dexterity": 4, "Recovery": 3, "Intellect": 1,
                "Creativity": 0, "Fear": 2, "Intimidation": -2,
                "Charisma": 2, "Stress": 1, "Health": -2,
                "Hunger": 0, "Energy": 1
                }),
    
    make_peep("Shown", 
              "Vengeful Targeter", 
              {
                "Strength": 2, "Defense": 1, "Evasion": 1,
                "Dexterity": 5, "Recovery": 0, "Intellect": -2,
                "Creativity": 4, "Fear": 3, "Intimidation": 3,
                "Charisma": 0, "Stress": -1, "Health": 1,
                "Hunger": -1, "Energy": 2
                }),
    
    make_peep("Ray", 
              "Silly Strongman", 
              {
                "Strength": 5, "Defense": 5, "Evasion": -4,
                "Dexterity": -2, "Recovery": 0, "Intellect": -4,
                "Creativity": 1, "Fear": 4, "Intimidation": 3,
                "Charisma": 3, "Stress": 3, "Health": 5,
                "Hunger": -3, "Energy": 2
                }),
    
    make_peep("Lito", 
              "Manipulating Deciever", 
              {
                "Strength": 3, "Defense": 3, "Evasion":2,
                "Dexterity": -3, "Recovery": -3, "Intellect": 1,
                "Creativity": -1, "Fear": 1, "Intimidation": 1,
                "Charisma": 5, "Stress": 3, "Health": 3,
                "Hunger": 1, "Energy": 2
                }),
    
    make_peep("Rebecca", 
              "Cowardly Outcast", 
              {
                "Strength": -1, "Defense": -1, "Evasion": 1,
                "Dexterity": 0, "Recovery": 3, "Intellect": 1,
                "Creativity": 1, "Fear": -3, "Intimidation": -4,
                "Charisma": -5, "Stress": 2, "Health": 8,
                "Hunger": -4, "Energy": 2
                }),
    
    make_peep("Cindy", 
              "Shallow Cleric", 
              {
                "Strength": -3, "Defense": 0, "Evasion": 3,
                "Dexterity": 2, "Recovery": 4, "Intellect": -3,
                "Creativity": 2, "Fear": 3, "Intimidation": -4,
                "Charisma": 3, "Stress": 2, "Health": 0,
                "Hunger": 6, "Energy": 3
                }),
    
    make_peep("Jayce", 
              "Hedonistic Tank", 
              {
                "Strength": 1, "Defense": 5, "Evasion": -3,
                "Dexterity": -4, "Recovery": -1, "Intellect": 1,
                "Creativity": 2, "Fear": 4, "Intimidation": -1,
                "Charisma": 4, "Stress": 1, "Health": 4,
                "Hunger": 0, "Energy": 5
                }),
    
    make_peep("Neo", 
              "The Jack of All Trades", 
              {
                "Strength": 1, "Defense": 2, "Evasion": 1,
                "Dexterity": 2, "Recovery": 3, "Intellect": 4,
                "Creativity": 2, "Fear": -1, "Intimidation": -3,
                "Charisma": 1, "Stress": 4, "Health": 2,
                "Hunger": 1, "Energy": -1
                }),
    
    make_peep("Jimmy", 
              "Independant Bully", 
              {
                "Strength": 4, "Defense": 4, "Evasion": 3,
                "Dexterity": 1, "Recovery": 1, "Intellect": 0,
                "Creativity": 2, "Fear": 4, "Intimidation": 4,
                "Charisma": -3, "Stress": -2, "Health": 4,
                "Hunger": -2, "Energy": -2
                }),
]

def print_peeps():
    for p in PEOPLE:
        print(p, "\n")
        
#print_peeps()