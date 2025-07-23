import visualization.graph_data as gd
import time as t
import copy
import peep_data.combo_db as cdb

from abc import ABC, abstractmethod

from peep_data.char_data import STAT_TYPES, SIMPLE_PEOPLE, get_peeps
from battle.stats import Stat

STAT_CHOICES = list(STAT_TYPES.keys())

class Simulator(ABC):
    
    EXIT_KEY = "exit"
    
    name = 'DID NOT SET NAME'
    funcs = ['DID NOT SET FUNCS']
    
    
    def simulate(self):
        print("\n")
            
        self.welcome()
        
        while True:
            print()
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
        print(f"\nExiting {self.name}. Goodbye!")
        t.sleep(1)
    
    def get_character_choice(self):
        return self.get_choice([p.name for p in SIMPLE_PEOPLE],
                               get_index=False)
    
    def get_choice(self, choices:list, get_index: bool = True, prompt: str = ""):
        '''
        Asks user to pick a choice from a list. 
        Continues to ask user until valid input is given.
        
        Parameters:
            choices (list): list of choices to pick from
            get_index (bool): whether to return index or reference of choice 
        
        Returns:
            Any: index or reference of choice
        '''
        
        valid = False
        choice = ""
        
        while not valid:
            for i, s in enumerate(choices):
                
                # format function names
                if callable(s):
                    s = s.__name__.replace("_", " ")
                    s = s[0].upper() + s[1:]
                    
                print(f"[{i+1}]", s)
            print(prompt)
            choice = input((f"Pick a number from  1-{len(choices)} \n")).lower()
            try:
                choice = int(choice) - 1
            except:
                continue
            valid = choice >= 0 and choice < len(choices)
            
        if get_index:
            return choice
        else:
            return choices[choice]
    
    def get_choice_with_exit(self, choices:list, prompt: str = ""):
        choices = copy.deepcopy(choices)
        choices.append(self.EXIT_KEY)
        choice = self.get_choice(choices=choices, get_index = False, prompt=prompt)
        
        if choice == self.EXIT_KEY:
            return None
        else:
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
                print(f"[{i+1}]", formatted_name)
                
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
        
        print("Which peep charts do you want to see? ")
        choice = self.get_character_choice()
            
        gd.show_spider_specific(choice)
        
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
            
            most_choice = ""
            least_choice = ""

            # input of desired stat         
            p = "Of these stat types, which do you value the most?"   
            most_choice = self.get_choice(STAT_CHOICES, get_index=False, prompt=p)

            # get list of stats excluding previously chosen stat
            valid_stats = STAT_CHOICES.copy()
            valid_stats.remove(most_choice)

            # input of sacrified stat
            p = "Of these stat types, which do you value the least?"
            least_choice = self.get_choice(valid_stats, get_index=False, prompt=p)
            
            if verbose:
                print("\nYou chose: " + most_choice + " and " + least_choice)
                
            results = cdb.get_specific_combo_n_runner_ups(most_choice, least_choice)
            
            #TODO: check for and communicate ties.
            
            winner = [p for p in SIMPLE_PEOPLE if p.name == results[0]["name"]][0]
            
            # print sorted people
            if verbose:
                print("\nContenders: ")
                for p in results:
                    print(p["name"] + ": " + str(p["diff"]))

            # TODO: perhaps only show the stats that the user chose?
            # Final answer
            print("\nYou got: " + str(winner) + "\n")
            self.obtained[winner] += 1
            t.sleep(2)
            
            # log choices
            self.history.append((most_choice, least_choice, winner.name))
            
            # print
            print("You have so far obtained:")
            for p in self.obtained:
                if self.obtained[p] == 0:
                    continue
                time_word_str = "times" if self.obtained[p] > 1 else "time"
                print(p.name + ": " + str(self.obtained[p]) + f" {time_word_str}!")
            t.sleep(1)
              
            # ask to play again or show history  
            continue_choice = 2      
            while continue_choice == 2:
                print("\nDo you want to play again?")
                continue_choice = self.get_choice(
                ["Yes, continue", 
                 "No, return to menu", 
                 "Show history and decide after"])  
                
                # history
                if continue_choice == 2:
                    print("\nHISTORY: ")
                    for c in self.history:
                        print(f"{c[0]} > {c[1]} = {c[2]}")
            # end loop    
                
            if continue_choice == 1:
                return
            
    
    def who_are_you_with_extra_info(self):
        self.who_are_you(True)
            
            
class DistSimulator(Simulator):
    def __init__(self):
        self.name = "Distribution of Stat Combos Simulator"
        self.funcs = [self.view_combos_by_peep, 
                      self.view_combos_by_major_stat, 
                      self.view_combos_by_lesser_stat, 
                      self.view_count_of_combos_per_peep, 
                      ]
    
    def view_combos_by_peep(self):
        self.view_combos_by([p.name for p in SIMPLE_PEOPLE], "name")
        
    def view_combos_by_major_stat(self):
        self.view_combos_by(STAT_CHOICES, "m_stat_name")
        
    def view_combos_by_lesser_stat(self):
        self.view_combos_by(STAT_CHOICES, "l_stat_name")
    
    def view_combos_by(self, choices: list, column_name: str):
        user_choices = choices[:]
        user_choices.append("All")
        c = self.get_choice(user_choices, get_index=False)
        if c != "All":
            print("\nCOMBOS BY " + c + " as " + column_name + ": ")
            results = cdb.get_combos_by(column_name, c)
            cdb.print_pretty_results(results, do_print_count=True)
            return
        
        print("\nALL COMBOS BY " + column_name + ": ")
        for elem in choices:
            print("\n" + elem + ": ")
            results = cdb.get_combos_by(column_name, elem)
            cdb.print_pretty_results(results, do_print_count=True)
    
    def view_count_of_combos_per_peep(self):
        print()
        results = cdb.get_count_of_combos_per_peep()
        cdb.print_pretty_results(results, do_print_count=True)
        
  
    def welcome(self):
        print(f"Welcome to the {self.name}!\n", 
              "Here you can view the different combinations of choosing a desired and undesired stat,"
              + "and what character would be obtained with that combo based on the character's stat aptitudes.",
              "These combos can be grouped by character, desired stat, or undesired stat.",
              "You can also view the count of how many combos there are to obtain each character.",
              "If you like looking at lots of data at once, you can view every permutation of combos grouped by your choosing.")
        t.sleep(1)    
        

class StatManipulationSimulator(Simulator):
    def __init__(self):
        self.name = "Stat Manipulation Simulator"
        self.peeps = copy.deepcopy(get_peeps())
        self.funcs = [self.play_with_peep_stats, self.play_with_equations] 
        
        self.peep_funcs = [self.manipulate_a_stat, self.get_peep_info, self.get_all_stat_info_of_peep
                           ,self.reset_peep_to_default]
        
        self.stat_funcs = [self.show_stat_info, self.apply_alteration, self.grow_or_shrink_stat, 
                           self.set_stat_values_directly, self.manipulate_apt_level_by_xp,
                           self.reset_stat_to_default]
        
    def welcome(self):
        print(f"Welcome to the {self.name}!\n",
              "Here you can manually change the stats of a character to get a feel for",
              "how stat values are calcuated.",
              "You can also view a deep dive of different equations used for stat calcuations.") 
        t.sleep(0.5)      
    
    def play_with_peep_stats(self):
        while True:
            prompt = "Which peep would you like to do stat experimentation on?"
            peep = self.get_choice_with_exit(self.peeps, prompt=prompt)
            
            if peep is None:
                return
            
            # TODO: choose to get peep info, hone in on a stat, or reset peep to default values
            prompt = f"What would you like to do with {peep.name}"
            peep_func = self.get_choice_with_exit(self.peep_funcs, prompt=prompt)
            
            if peep_func is None:
                continue
            
            peep_func(peep)
    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PEEP FUNCTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''        
    def get_peep_info(self, peep):
        pass
    
    def get_all_stat_info_of_peep(self, peep):
        pass
    
    def reset_peep_to_default(self, peep):
        pass
    
    def manipulate_all_stats(self, peep):
        pass
    
    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~STAT MANIPULATION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    
    def manipulate_a_stat(self, peep):
        
        while True:
            prompt = f"Which stat of {peep.name} would you like to manipulate"
            stat_name = self.get_choice_with_exit(STAT_CHOICES, prompt=prompt)
            
            if stat_name is None:
                return
            
            stat = peep.get_stat(stat_name)
            
            while True:
                # choose different funcs of manipulating the stat
                prompt = f"What would you like to do with the {stat_name} stat?"
                chosen_func = self.get_choice_with_exit(self.stat_funcs, prompt=prompt) 
                
                if chosen_func is None:
                    break
                
                chosen_func(stat)     
       
    def set_stat_values_directly(self, stat:Stat):
        pass
    
    def grow_or_shrink_stat(self, stat:Stat):
        pass
    
    def manipulate_apt_level_by_xp(self, stat:Stat):
        pass
    
    def show_stat_info(self, stat:Stat):
        print("AHHHHH")
        pass
    
    def reset_stat_to_default(self, stat:Stat):
        pass
    
    def apply_alteration(self, stat:Stat):
        pass
    
    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EQUATIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    def play_with_equations(self):
        pass
       
    '''
    First, choose peep to experiment on
    Options:
        see all stat info of peep
        reset all stats to default
        choose a stat to start manipulating
        Stat Options:
            you can add debuffs or buffs of custom values (within reason)
            set/grow/shrink the apt and values
            allow for easy tweaks when new ways to modify multiplier are added
            you can level down/up aptitudes
            see different equations and their steps for stat calculating
            reset this stat to default
    Changes are only saved for the session
    
    '''
    