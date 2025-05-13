from peep_data.char_data import STAT_TYPES, SIMPLE_PEOPLE, sort_peeps, get_highest_diff_peep
from battle.intiative_sim import start_round
import peep_data.char_data as char_data
import visualization.graph_data as gd

# read character data and populate SIMPLE_PEOPLE
char_data.peep_fetch()

'''
TODO: cli interface that allows to move up back to main loop

'''

STAT_NAMES = STAT_TYPES.keys()

def question_main():
    while True:

        print("\n")
        
        valid = False
        most_choice = ""
        least_choice = ""

        # get input that is a valid choice 
        # (converted into format that compares to str in STAT_NAMES)
        while not valid:
            most_choice = input(("Of these choices, what do you value the most? " + 
                                 ", ".join(STAT_NAMES) + ": ")).lower()
            #most_choice = most_choice[0].upper() + most_choice[1:]   
            valid = most_choice in STAT_NAMES

        # get list of stats excluding previously chosen stat
        valid_stats = STAT_NAMES.copy()
        valid_stats.remove(most_choice)
        
        valid = False

        # input of sacrified stat
        while not valid:
            least_choice = input(("Of these choices, what do you value the least? " + 
                                  ", ".join(valid_stats) + ": ")).lower()
            #least_choice = least_choice[0].upper() + least_choice[1:]  
            valid = least_choice in valid_stats
            
        # sort people by chosen stats!! based on difference between them
        sorted_people = sort_peeps(SIMPLE_PEOPLE, most_choice, least_choice)
        
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
        

def graph_main():
    
    while True:
        print("\n")
        
        valid = False
        choice = ""

        # input
        while not valid:
            choice = input(("Do you want to see spider charts of all character's "
                            "Emotional, Physical, ALL stats, or a specific character?")).lower()
            valid = choice in ["emotional", "emo", "phys","physical", "all", "one", "specific"]

        valid = False
        
        if choice in ["emotional", "emo"]:
            gd.show_spider_emotion()
            continue
        elif choice in ["phys", "physical"]:
            gd.show_spider_physical()
            continue
        elif choice in ["all"]:
            gd.show_spider_all()
            continue
        

        # get input that is a specific char name
        while not valid:
            choice = input("Which char charts do you want to see? " + ", ".join([p.name for p in SIMPLE_PEOPLE]) + ": ").lower()
            valid = [p for p in SIMPLE_PEOPLE if p.name.lower() == choice]
        
        validated_choice = choice[0].upper() + choice[1:]    
            
        gd.show_spider_specific(validated_choice)
    
def dist_main():
    
    char_data.get_distribution()   
    
    while True:
        print("\n")
        
        valid = False
        choice = ""

        # input
        while not valid:
            choice = input(("See character distribution by Peep, "
                            "Desired Choice, or Least Choice? ")).lower()
            valid = choice in ["peep", "p", "desired", "most", "m", "least", "l"]
            
        if choice in ["peep", "p"]:
            char_data.print_combos_by_peep()
        elif choice in ["desired", "most", "m"]:
            char_data.print_combos_by_M_stat()
        elif choice in ["least", "l"]:
            char_data.print_combos_by_L_stat() 
            
        char_data.print_distribution()

def init_main():
    while True:
        start_round()
        input("Press enter to continue")

def main():
    print("\n")
        
    valid = False
    choice = ""

    # input
    while not valid:
        choice = input(("See questions, graphs, distributions, or init sim? (q,g,d,i)")).lower()
        valid = choice in ["q", "g", "d", "i"]
        
    if choice == "q":
        question_main()
    elif choice == "g":
        graph_main()
    elif choice == "d":
        dist_main()
    elif choice == "i":
        init_main()

if __name__ == "__main__": main()