from .character import Character
from peep_data.data_reader import PEEPS

#STAT_NAMES = STAT_TYPES.keys()

''' -------------------------------UNUSED but may be useful in the future-------------------------------'''

'''
# Gets average difference between stats for each character, and their overall average
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
   
# Prints average stat differences
def print_avg_stats():
    set_avg_stat_diff()
    
    for p in SIMPLE_PEOPLE:
        print("\n" + p.name + ": ")
        for stat in p.avg_stat_diffs:
            print(stat, p.avg_stat_diffs[stat])
        print("\nTotal Difference Avg: " + str(p.avg_diff))
        print("\n-----------------------------")
'''