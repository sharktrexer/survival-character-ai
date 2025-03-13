from preset_characters import STAT_NAMES, PEOPLE

# dictionary to keep track of how many times a character can be selected based on choosing
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
   
def print_avg_stats():
    set_avg_stat_diff()
    
    for p in PEOPLE:
        print("\n" + p.name + ": ")
        for stat in p.avg_stat_diffs:
            print(stat, p.avg_stat_diffs[stat])
        print("\nTotal Difference Avg: " + str(p.avg_diff))
        print("\n-----------------------------")
  
#print_avg_stats()

# sort peeps by difference between most and least choice
def sort_peeps(peeps: list, most_choice: str, least_choice: str) -> list:
    sorted_peeps = sorted(peeps, key=lambda p: -(p.stats[most_choice] - p.stats[least_choice]))
    return sorted_peeps

# sort peeps with highest stat
def get_highest_stat(peeps: list, stat: str) -> str:
    sorted_peeps = sorted(peeps, key=lambda p: -p.stats[stat])
    return sorted_peeps

# get character distribution
def get_distribution(peeps: list) -> dict:
    for m_stat in STAT_NAMES:
        for l_stat in STAT_NAMES:
            if m_stat != l_stat:
                sorted_people = sort_peeps(PEOPLE, m_stat, l_stat)
                top_peep_diff = sorted_people[0].stats[m_stat] - sorted_people[0].stats[l_stat]
                next_peep_diff = sorted_people[1].stats[m_stat] - sorted_people[1].stats[l_stat]
                highest_peep = [sorted_people[0]]
                
                if top_peep_diff == next_peep_diff:
                    highest_peep = get_highest_stat(sorted_people[:2], m_stat)
                character_count[highest_peep[0].name] += 1
                
                # Store stat combo in character that would be selected
                highest_peep[0].stat_combos.append((m_stat, l_stat))

get_distribution(PEOPLE)

def print_combos():
    
    for p in PEOPLE:
        print("\n" + p.name + " " + str(len(p.stat_combos)) + ": ")
        for stat in p.stat_combos:
            print(stat[0], stat[1])
        print("\n-----------------------------")

print_combos()

def print_distribution():

    print("\nCharacter distribution:")
    for key in character_count:
        print(key, character_count[key])

    print("\n")

print_distribution()
# main loop
def main():
    while True:

        valid = False
        most_choice = ""
        least_choice = ""

        # get input that is a valid choice
        while not valid:
            most_choice = input("Of these choices, what do you value the most? " + ", ".join(STAT_NAMES) + ": ")
            valid = most_choice in STAT_NAMES

        # get list of stats excluding previously chosen stat
        valid_stats = STAT_NAMES.copy()
        valid_stats.remove(most_choice)
        
        valid = False

        # input of sacrified stat
        while not valid:
            least_choice = input("Of these choices, what do you value the least? " + ", ".join(valid_stats) + ": ")
            valid = least_choice in valid_stats
            
        # sort people by chosen stats!! based on difference between them
        sorted_people = sort_peeps(PEOPLE, most_choice, least_choice)

        # tiebreaker:
        # if 2 have same difference, choose the one with the highest desired stat
        # TODO: check for a tie!!!
        top_peep_diff = abs(sorted_people[0].stats[most_choice] - sorted_people[0].stats[least_choice])
        next_peep_diff = abs(sorted_people[1].stats[most_choice] - sorted_people[1].stats[least_choice])
        top_people = [sorted_people[0]]
        
        if top_peep_diff == next_peep_diff:
            top_people = get_highest_stat(sorted_people[:2], most_choice)

        for peep in sorted_people:
            print(peep.name)

        print("\n")

        for peep in top_people:
            print(peep.name)

        print("\nYou got: " + str(top_people[0]))
        
#main()
