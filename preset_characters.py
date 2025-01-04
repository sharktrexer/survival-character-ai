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

def make_peep(name: str, desc: str, stat_vals: list):
    '''Easily creates characters while verifying they have the right amount of stat distribution'''
    val_total = sum(stat_vals)
    
    if (val_total != MAX_STAT_VAL and (name == "Rebecca" and val_total != 0)):
        raise Exception(f"Character \"{name}\" does not have a total of {MAX_STAT_VAL} points in their stats, but instead {val_total}")
    
    return Character(name, desc, dict(zip(STAT_NAMES, stat_vals)))

''' 
List of preset characters

Combines stat name list with numerical values to create and
store dictionary of customized stats with associated names
'''
PEOPLE = [
    make_peep("Chris", 
              "Perfectionist", 
              [
                4,3,-2,
                1,-1,2,
                5,0,1,
                1,-2,4,
                -1,3
                ]),
    
    make_peep("Adan", 
              "Handsome Rogue", 
              [
                0,2,5,
                4,2,1,
                1,1,-2,
                2,1,0,
                0,1
                ]),
    
    make_peep("Shown", 
              "Vengeful", 
              [
                2,1,2,
                5,1,-2,
                4,3,1,
                0,-1,1,
                -1,2
                ]),
    
    make_peep("Ray", 
              "Himbo", 
              [
                5,5,-3,
                -2,0,-4,
                0,4,3,
                3,3,5,
                -3,2
                ]),
    
    make_peep("Lito", 
              "Manipulator", 
              [
                3,3,2,
                -3,2,1,
                -3,1,1,
                4,3,3,
                1,0
                ]),
    
    make_peep("Rebecca", 
              "Outcast", 
              [
                -1,-1,1,
                0,3,1,
                1,-3,-4,
                -5,2,5,
                -4,5
                ]),
    
    make_peep("Cindy", 
              "Shallow", 
              [
                -4,1,3,
                3,5,-4,
                2,3,-4,
                4,2,0,
                3,4
                ]),
    
    make_peep("Jayce", 
              "Entertainer", 
              [
                2,2,4,
                -2,1,2,
                2,0,0,
                3,-2,1,
                2,3
                ]),
    
    make_peep("Leo", 
              "Blank Slate", 
              [
                1,2,2,
                2,3,4,
                2,-1,-3,
                1,3,2,
                1,-1
                ]),
    
    make_peep("Jimmy", 
              "Bully", 
              [
                4,4,4,
                1,1,0,
                2,3,4,
                -3,-2,4
                -2,-2
                ]),
]

def print_peeps():
    for p in PEOPLE:
        print(p, "\n")
        
print_peeps()