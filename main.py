from preset_characters import STAT_NAMES, PEOPLE



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
