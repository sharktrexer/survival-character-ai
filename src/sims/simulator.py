import visualization.graph_data as gd
import time as t

from abc import ABC, abstractmethod

from peep_data.char_data import (
    STAT_TYPES, 
    SIMPLE_PEOPLE, 
    sort_peeps, 
    get_highest_diff_peep, 
    get_distribution, 
    print_combos_by_peep, 
    print_combos_by_M_stat, 
    print_combos_by_L_stat, 
    print_distribution_count
    )

class Simulator(ABC):
    
    EXIT_KEY = "exit"
    
    name = 'DID NOT SET NAME'
    funcs = ['DID NOT SET FUNCS']
    
    
    def simulate(self):
        print("\n")
            
        self.welcome()
        
        while True:
            print("")
            exit_code = self.choose_func()
            if exit_code == 0:
                return
            t.sleep(0.5)
    
    @abstractmethod
    def welcome(self):
        raise NotImplementedError("Welcome method must be implemented in simulator subclass.")
        
    def notify_of_option_to_exit(self):
        print(f"Enter {self.EXIT_KEY} to exit this simulation.")
    
    def validate_exit(self, user_in: str):
        return user_in.lower().strip() == self.EXIT_KEY
    
    def goodbye(self):
        print(f"Exiting {self.name}. Goodbye!")
        t.sleep(1)
    
    def get_choice(self, choices:list):
        '''
        Asks user to pick a choice from a list. 
        Continues to ask user until valid input is given.
        
        Parameters:
            choices (list): list of choices to pick from
        
        Returns:
            int: index of choice
        '''
        
        valid = False
        choice = ""
        
        while not valid:
            for i, s in enumerate(choices):
                print(s, f"[{i+1}]")
            choice = input((f"Pick a number from  1-{len(choices)} \n")).lower()
            try:
                choice = int(choice) - 1
            except:
                continue
            valid = choice >= 0 and choice < len(choices)
        return choice
    
    def choose_func(self):
        '''
        Asks user to pick a function to run from self.funcs. If user enters self.EXIT_KEY,
        ends the simulation and says goodbye. If not, calls the function and returns 1.
        Otherwise, continues to ask user until valid input is given.
        
        Returns:
            int: 0 if user wants to exit, 1 otherwise
        '''
        valid = False
        choice = ""
        
        while not valid:
            for i, s in enumerate(self.funcs):
                formatted_name = s.__name__.replace("_", " ")
                formatted_name = formatted_name[0].upper() + formatted_name[1:]
                print(formatted_name, f"[{i+1}]")
                
            self.notify_of_option_to_exit()
            choice = input((f"Pick a number from  1-{len(self.funcs)} \n")).lower()
            
            if self.validate_exit(choice):
                self.goodbye()
                return 0
            
            try:
                choice = int(choice) - 1
            except:
                continue
            valid = choice >= 0 and choice < len(self.funcs)
            
            self.funcs[choice]()
            return 1
    
class GraphSimulator(Simulator):
    
    def __init__(self):
        self.name = "Spider Graph Simulator"
        self.funcs = [gd.show_spider_emotion,
                gd.show_spider_physical,
                gd.show_spider_all,
                self.get_specific_spider]
    
    def get_specific_spider(self):
        valid = False
        choice = ""
        while not valid:
            choice = input("Which peep charts do you want to see? " + ", ".join([p.name for p in SIMPLE_PEOPLE]) + ": ").lower()
            valid = [p for p in SIMPLE_PEOPLE if p.name.lower() == choice]
        
        validated_choice = choice[0].upper() + choice[1:]    
            
        gd.show_spider_specific(validated_choice)
        
    def welcome(self):
        print(f"Welcome to the {self.name}!\n", 
              "Here you will be able to see a visualization of each character's stats.",
              "You can choose to see spider charts of all character's Emotional, Physical,",
              "or ALL stats, or each of those charts for a specific character.")
        t.sleep(1)
    


class WhoAreYouSimulator(Simulator):
    
    def __init__(self):
        self.name = "Who Are You Simulator"
        self.funcs = [self.who_are_you, self.who_are_you_with_extra_info]
        self.stat_choices = list(STAT_TYPES.keys())
        self.obtained = {key: 0 for key in SIMPLE_PEOPLE}
        self.history = []

    def welcome(self):
        print(f"Welcome to the {self.name}!\n", 
              "Here you will choose a stat you value the most and the stat you value the least.",
              "Based on those choices, you will obtain a character that fits your preferences.",
              "Specifically, the given character will have the highest difference between your chosen stats.",
              "Before you get started, you can choose to play normally or with extra information detailing how the character was chosen.",)
        t.sleep(1)
    
    def who_are_you(self, verbose: bool = False):
        while True:
            
            valid = False
            most_choice = ""
            least_choice = ""

            # input of desired stat         
            print("Of these stat types, which do you value the most?")    
            most_choice = self.stat_choices[self.get_choice(self.stat_choices)]

            # get list of stats excluding previously chosen stat
            valid_stats = self.stat_choices.copy()
            valid_stats.remove(most_choice)
            
            valid = False

            # input of sacrified stat
            print("Of these stat types, which do you value the least?")
            least_choice = valid_stats[self.get_choice(valid_stats)]
            
            if verbose:
                print("\nYou chose: " + most_choice + " and " + least_choice)
                
            # sort people by chosen stats!! based on difference between them
            sorted_people = sort_peeps(SIMPLE_PEOPLE, most_choice, least_choice)
            
            # print sorted people
            if verbose:
                print("\nContenders: ")
                for p in sorted_people:
                    print(p.name + ": " + str(p.stat_apts[most_choice] - p.stat_apts[least_choice]))

            # tiebreaker:
            top_peeps = get_highest_diff_peep(sorted_people, most_choice, least_choice)
            
            if verbose:
                print("\nTOP 3: ")
                for p in top_peeps:
                    print(p.name + ": " + str(p.stat_apts[most_choice] - p.stat_apts[least_choice]))

            # TODO: perhaps only show the stats that the user chose?
            # Final answer
            print("\nYou got: " + str(top_peeps[0]) + "\n")
            self.obtained[top_peeps[0]] += 1
            t.sleep(2)
            
            # log choices
            self.history.append((most_choice, least_choice, top_peeps[0].name))
            
            # print
            print("You have so far obtained:")
            for p in self.obtained:
                if self.obtained[p] == 0:
                    continue
                print(p.name + ": " + str(self.obtained[p]) + " times!")
            t.sleep(1)
              
            # ask to play again or show history          
            valid = False
            while not valid:
                continue_choice = input("Play Again? (y/n) or show history? (h): ").lower()
                valid = continue_choice in ["y", "n", "h"]
                
                # show history and ask again to play
                if valid and continue_choice == "h":
                    print("\nHISTORY: ")
                    for c in self.history:
                        print(f"{c[0]} > {c[1]} = {c[2]}")
                    print("\n")
                    valid = False
                
            if continue_choice == "n":
                return
            
    
    def who_are_you_with_extra_info(self):
        self.who_are_you(True)
            
            
class DistSimulator(Simulator):
    def __init__(self):
        self.name = "Distribution of Stat Combos Simulator"
        self.funcs = [print_combos_by_peep, 
                      print_combos_by_M_stat, 
                      print_combos_by_L_stat, 
                      print_distribution_count]
        
        get_distribution()
        
    def welcome(self):
        print(f"Welcome to the {self.name}!\n", 
              "Here you can view the different combinations of a chosen desired and undesired stat,"
              + "and what character would be obtained with that combo.",
              "These combos can be grouped by character, desired stat, or undesired stat.",
              "You can also just view how many combos there are to obtain each character.",
              "Keep in mind this is a very rough implementation without much styling.")
        t.sleep(1)    
        

            

        
    