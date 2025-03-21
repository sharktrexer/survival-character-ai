from char_data import STAT_NAMES, PEOPLE, sort_peeps, get_highest_diff_peep
import char_data
import graph_data as gd

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
        
        # print sorted people
        print("\nSORTED ")
        for p in sorted_people:
            print(p.name + ": " + str(p.stats[most_choice] - p.stats[least_choice]))

        # tiebreaker:
        top_peeps = get_highest_diff_peep(sorted_people, most_choice, least_choice)
        
        print("\nTOP 3")
        for p in top_peeps:
            print(p.name + ": " + str(p.stats[most_choice] - p.stats[least_choice]))

        print("\nYou got: " + str(top_peeps[0]) + "\n")
        

char_data.get_distribution()

#char_data.print_combos_by_peep()
#char_data.print_combos_by_M_stat()
#char_data.print_combos_by_L_stat()

#char_data.print_distribution()

gd.show_spider_all()
#gd.show_spider_physical()
#gd.show_spider_emotion()

#main()
