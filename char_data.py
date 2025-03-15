from character import Character

# List of all the stat names used by characters
STAT_NAMES = [
        "Strength", "Defense", "Evasion",   
                
        "Dexterity", "Recovery", "Intellect", 
        
        "Creativity", "Fear", "Intimidation",
        
        "Charisma", "Stress", "Health", 
        
        "Hunger", "Energy", 
    ]

# Max amount of points that can be distributed amongst character stats
MAX_STAT_VAL = 18

def make_peep(name: str, desc: str, stats: dict):
    '''Easily creates characters while verifying they have the right amount of stat distribution'''
    val_total = sum(stats.values())
    
    # Rebecca has a special case
    val_total = MAX_STAT_VAL if name == "Rebecca" and val_total == 0 else val_total
    
    if val_total != MAX_STAT_VAL:
        raise Exception(f"Character \"{name}\" does not have a total of {MAX_STAT_VAL} points in their stats, but instead {val_total}")
    
    return Character(name, desc, stats)


# List of preset characters

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

''' Prints all character names, titles, and stats '''
def print_peeps():
    for p in PEOPLE:
        print(p, "\n")

# dictionary to keep track of how many ways a character can be selected based on choosing
# 2 stats to uphold and discard
character_count = {
    "Chris" : 0,
    "Adan" : 0,
    "Shown" : 0,
    "Ray" : 0,
    "Lito" : 0,
    "Rebecca" : 0,
    "Cindy" : 0,
    "Jayce" : 0,
    "Neo" : 0,
    "Jimmy" : 0,
}

# Stores list of combos and their resulting character
combos = []

''' Class to store combo of peep, desired stat, undesired stat, and runner ups '''
class combo:
    def __init__(self, peep, m_stat, l_stat, runner_ups):
        self.peep = peep
        self.m_stat = m_stat
        self.l_stat = l_stat
        self.runner_ups = runner_ups
        
    def __str__(self):
        return (self.peep.str_difference(self.m_stat, self.l_stat) + " | \t\t"
                + self.runner_ups[0].str_difference(self.m_stat, self.l_stat, is_simple=True) + " | \t"
                + self.runner_ups[1].str_difference(self.m_stat, self.l_stat, is_simple=True)
                )
        
    ''' String format for sorting by discarded stat '''
    def str_lesser(self):
        return (self.peep.str_difference(self.l_stat, self.m_stat, is_reversed=True)  + " | \t\t"
                + self.runner_ups[0].str_difference(self.m_stat, self.l_stat, is_reversed=True, is_simple=True) 
                + " | \t"
                + self.runner_ups[1].str_difference(self.m_stat, self.l_stat, is_reversed=True, is_simple=True)
                )
        
    ''' String format to exclude peep name'''
    def str_simple(self):
      return (self.peep.str_difference(self.m_stat, self.l_stat, no_name=True) + " | \t\t"
                + self.runner_ups[0].str_difference(self.m_stat, self.l_stat, is_simple=True) + " | \t"
                + self.runner_ups[1].str_difference(self.m_stat, self.l_stat, is_simple=True)
                )
      
'''Gets average difference between stats for each character, and their overall average'''
def set_avg_stat_diff():
    for p in PEOPLE:
        total_avg = 0
        for stat in STAT_NAMES:
            avg = 0
            for other_stat in STAT_NAMES:
                if stat != other_stat:
                    diff = abs(p.stats[stat] - p.stats[other_stat])
                    avg += diff
            avg = round(avg / (len(STAT_NAMES) - 1), 2)
            avg = round(avg, 2)
            p.avg_stat_diffs[stat] = avg
            total_avg += avg
        p.avg_diff = round(total_avg / len(STAT_NAMES), 2)
   
'''Prints average stat differences'''
def print_avg_stats():
    set_avg_stat_diff()
    
    for p in PEOPLE:
        print("\n" + p.name + ": ")
        for stat in p.avg_stat_diffs:
            print(stat, p.avg_stat_diffs[stat])
        print("\nTotal Difference Avg: " + str(p.avg_diff))
        print("\n-----------------------------")

''' In progress func to test other ways of calculating difference '''
def diff_of_stats(peep, m_stat, l_stat):
    
    most_stat = peep.stats[m_stat]
    least_stat = peep.stats[l_stat]
    
    larger_stat = most_stat if most_stat > least_stat else least_stat
    smaller_stat = least_stat if most_stat > least_stat else most_stat
    
    if peep.m_stat > 0 and peep.l_stat > 0 or peep.m_stat < 0 and peep.l_stat < 0:
        return most_stat, abs(smaller_stat) - abs(larger_stat)
    else:
        return most_stat, abs(most_stat) + abs(least_stat)

''' sort peeps by difference between most and least choice '''
def sort_peeps(peeps: list, most_choice: str, least_choice: str) -> list:
    sorted_peeps = sorted(peeps, key=lambda p: -(p.stats[most_choice] - p.stats[least_choice]))
    return sorted_peeps
#TODO: get 2 lists, 1 sorted by highest wanted stat and 1 sorted by lowest discarded stat
# Pick character with highest difference of indexes between 2 lists.

''' sort peeps by highest stat, used as a tiebreaker '''
def get_highest_stat(peeps: list, stat: str) -> str:
    sorted_peeps = sorted(peeps, key=lambda p: -p.stats[stat])
    return sorted_peeps

''' gets peep with highest difference between most and least desired choice.
Chooses peep with the highest desired stat of top 3 if there is a tie
'''
def get_highest_diff_peep(sorted_peeps: list, m_stat: str, l_stat: str) -> list:
  top_peep_diff = sorted_peeps[0].stats[m_stat] - sorted_peeps[0].stats[l_stat]
  next_peep_diff = sorted_peeps[1].stats[m_stat] - sorted_peeps[1].stats[l_stat]
  highest_peeps = sorted_peeps[:3]
  
  if top_peep_diff == next_peep_diff:
      highest_peeps = get_highest_stat(highest_peeps, m_stat)
      
  return highest_peeps

''' calculates character distribution based on 2 chosen stats, 
and the stat combos that would be selected '''
def get_distribution() -> dict:
    for m_stat in STAT_NAMES:
        for l_stat in STAT_NAMES:
            if m_stat != l_stat:
                sorted_people = sort_peeps(PEOPLE, m_stat, l_stat)
                # tiebreaker
                top_peeps = get_highest_diff_peep(sorted_people, m_stat, l_stat)
                top_peep = top_peeps[0]
                character_count[top_peep.name] += 1
                
                # Store general combo
                combos.append(combo(top_peep, m_stat, l_stat, top_peeps[1:]))
                
                # Store stat combo in character that would be selected
                #top_peep.stat_combos.append((m_stat, l_stat))

''' Prints combos grouped by most stat'''
def print_combos_by_M_stat():
    print("\Combinations by desired stat:")
    for combo in combos:
        print(combo)

''' Prints combos grouped by lesser stat'''
def print_combos_by_L_stat():
    print("\nCombinations by undesired stat:")
    l_combos = sorted(combos, key=lambda c: c.l_stat)
    for combo in l_combos:
        print(combo.str_lesser())
    
''' Prints combos grouped by peep'''
def print_combos_by_peep():
    print("\Combinations by character:")
    p_combos = sorted(combos, key=lambda c: c.peep.name)
    cur_name = ""
    for combo in p_combos:
        if cur_name != combo.peep.name:
            print(("\n--------------------\n\n\t\t<" + combo.peep.name + "> " 
                   + str(character_count[combo.peep.name]) + ": "))
            cur_name = combo.peep.name
        print(combo.str_simple())

''' Prints character names and how many times they would be selected based on 2 stat choices'''
def print_distribution():

    print("\nCharacter distribution:")
    for key in character_count:
        print(key, character_count[key])

    print("\n")