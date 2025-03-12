from preset_characters import STAT_NAMES, PEOPLE

# dictionary to keep track of what character the player is most like
user_inclinations = {
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
    sorted_people = sorted(PEOPLE, key=lambda p: -(p.stats[most_choice] - p.stats[least_choice]))

    # tiebreaker
    top_people = sorted(sorted_people[:2], key=lambda p: -p.stats[most_choice])

    for peep in sorted_people:
        print(peep.name)

    print("\n\n")

    for peep in top_people:
        print(peep.name)

    print("\nYou got: " + str(top_people[0]))
