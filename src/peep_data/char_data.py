from .character import Character
from peep_data.data_reader import STAT_TYPES, get_peeps

STAT_NAMES = STAT_TYPES.keys()

# List of all the character descriptions
CHAR_DESC = ["Nourishing Paladin", "Benevolent Assassin", "Vengeful Tinkerer",
             "Unserious Wrestler", "Manipulating Incubus", "Uncouth Coward",
             "Promiscuous Dancer", "Protector of Parties", "Calm Sorcerer",
             "Domineering Barbarian"]

# Max amount of points that can be distributed amongst character stats
MAX_STAT_VAL = 18

# List of Characters with only their aptitudes
SIMPLE_PEOPLE = []


def make_peep(name: str, desc: str, stats: dict):
    '''Easily creates characters while verifying they have the right amount of stat distribution'''
    val_total = sum(stats.values())
    
    # Rebecca has a special case
    val_total = MAX_STAT_VAL if name == "Rebecca" and val_total == 0 else val_total
    
    if val_total != MAX_STAT_VAL:
        raise Exception(f"Character \"{name}\" does not have a total of {MAX_STAT_VAL} points in their stats, but instead {val_total}")
    
    return Character(name, desc, stats)

def get_peeps_as_simple():
    """
    Transforms a list of BattlePeep objects into Character objects with only stat aptitudes.

    Retrieves peeps from the data reader, converts them into Character instances 
    with a predefined description and a simplified dictionary of their stats, 
    and appends them to the PEOPLE list.
    """
    complex_peeps = get_peeps()
    for i, bp in enumerate(complex_peeps):
        SIMPLE_PEOPLE.append(make_peep(bp.name, CHAR_DESC[i], 
                                bp.get_stat_apts()))
    

''' Prints all character names, titles, and stats '''
def print_peeps():
    for p in SIMPLE_PEOPLE:
        print(p, "\n")





''' UNUSED but may be useful in the future'''

'''Gets average difference between stats for each character, and their overall average'''
def set_avg_stat_diff():
    for p in SIMPLE_PEOPLE:
        total_avg = 0
        for stat in STAT_NAMES:
            avg = 0
            for other_stat in STAT_NAMES:
                if stat != other_stat:
                    diff = abs(p.stat_apts[stat] - p.stat_apts[other_stat])
                    avg += diff
            avg = round(avg / (len(STAT_NAMES) - 1), 2)
            avg = round(avg, 2)
            p.avg_stat_diffs[stat] = avg
            total_avg += avg
        p.avg_diff = round(total_avg / len(STAT_NAMES), 2)
   
'''Prints average stat differences'''
def print_avg_stats():
    set_avg_stat_diff()
    
    for p in SIMPLE_PEOPLE:
        print("\n" + p.name + ": ")
        for stat in p.avg_stat_diffs:
            print(stat, p.avg_stat_diffs[stat])
        print("\nTotal Difference Avg: " + str(p.avg_diff))
        print("\n-----------------------------")
