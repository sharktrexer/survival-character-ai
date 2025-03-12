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
                highest_peep = get_highest_stat(sorted_people[:2], m_stat)
                character_count[highest_peep[0].name] += 1

get_distribution(PEOPLE)

print("\nCharacter distribution:")
for key in character_count:
    print(key, character_count[key])

# main loop
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
    #sorted_people = sorted(PEOPLE, key=lambda p: -(p.stats[most_choice] - p.stats[least_choice]))
    sorted_people = sort_peeps(PEOPLE, most_choice, least_choice)

    # tiebreaker:
    # if 2 have same difference, choose the one with the highest desired stat
    #top_people = sorted(sorted_people[:2], key=lambda p: -p.stats[most_choice])
    top_people = get_highest_stat(sorted_people[:2], most_choice)

    for peep in sorted_people:
        print(peep.name)

    print("\n\n")

    for peep in top_people:
        print(peep.name)

    print("\nYou got: " + str(top_people[0]))
