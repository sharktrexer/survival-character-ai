import visualization.graph_data as gd
import time as t
import copy
import peep_data.combo_db as cdb

from abc import ABC, abstractmethod
from typing import Callable

from peep_data.data_reader import SIMPLE_PEEPS, PEEPS
from battle.stats import Stat, STAT_TYPES
from battle.battle_peep import BattlePeep
from battle.peep_manager import PeepManager

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
            t.sleep(0.2)
    
    @abstractmethod
    def welcome(self):
        raise NotImplementedError("Welcome method must be implemented in simulator subclass.")
        
    def notify_of_option_to_exit(self):
        print(f"Enter {self.EXIT_KEY} to exit.")
    
    def validate_exit(self, user_in: str):
        return user_in.lower().strip() == self.EXIT_KEY
    
    def goodbye(self):
        print(f"\nExiting {self.name}. Goodbye!")
        t.sleep(0.2)
    
    def get_character_choice(self):
        return self.get_choice([p.name for p in SIMPLE_PEEPS],
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
        print()
        
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
        
        print()
            
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
    
    def obtain_number_inputs(self, input_form_dict:dict, conds:list[Callable[[float], bool]] = []):
        
        """
        Asks user to enter a certain number of numbers separated by spaces. Can specify 
        conditions for each input number. If user enters self.EXIT_KEY, ends the input process 
        and returns False. If user enters an invalid number of inputs, or if any of the inputs 
        do not meet the associated condition, asks user again. If user enters valid inputs, 
        updates the input_form_dict with the inputs.
        
        Parameters:
            input_form_dict (dict): dictionary to store the inputs. Keys are the names of the inputs
            conds (list[function]): list of functions to check the inputs against. The i-th function takes
                the i-th input as an argument and returns a boolean
        Returns:
            bool: True if inputs are valid, False if user wants to exit
        """
        
        if len(input_form_dict.keys()) != len(conds):
            raise ValueError("Number of inputs and conditions must be equal. Use None for no condition.")
        
        req_num_of_ins = len(input_form_dict.keys())
        
        while True:
            print("Enter " + str(req_num_of_ins) + " numbers separated by spaces: ")
            user_nums = input().split()
            
            if user_nums == []:
                print("No input received.")
                continue
            
            if user_nums[0] == self.EXIT_KEY:
                return False
                        
            if len(user_nums) < req_num_of_ins or len(user_nums) > req_num_of_ins:
                print("Incorrect number of inputs received: " + str(len(user_nums)) + " instead of " + str(req_num_of_ins))
                continue
            
            valid = True
            for i, key in enumerate(input_form_dict.keys()):
                try:
                    cast = float(user_nums[i])
                    
                    # check associated condition
                    if conds[i] is not None:
                        valid = conds[i](cast)
                        if not valid:
                            print("Input does not meet conditions.")
                            valid = False
                            break
                    
                    input_form_dict[key] = cast
                except:
                    print("Non-number input recieved.")
                    valid = False
                    break
            
            if not valid:
                continue
                
            return True
    
    def mini_sim(self, *, func_list:list[Callable], args:list, prompt: str = ""):    
        """
        Run a mini simulation where the user is given a list of functions
        to choose from. The chosen function is then called with the provided
        arguments. If the user chooses to exit, the function returns None.
        
        Parameters:
            func_list (list[function]): list of functions to choose from
            args (list): arguments to pass to the chosen function
            prompt (str, optional): prompt to display when asking for user input. Defaults to "".
        """

        while True:
            # choose different funcs to pass args to
            print(prompt)
            chosen_func = self.get_choice_with_exit(func_list, prompt) 
            
            if chosen_func is None:
                return
                
            chosen_func(*args)     
 
'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
'''   
    
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
        print(f"Welcome to the {self.name}!", 
              "\nHere you will be able to see a visualization of each character's stats.",
              "You can choose to see spider charts of all character's Emotional, Physical,",
              "or ALL stats, or each of those charts for a specific character.")
        t.sleep(0.2)
 
'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
'''   

class WhoAreYouSimulator(Simulator):
    
    def __init__(self):
        self.name = "Who Are You Simulator"
        self.funcs = [self.who_are_you, self.who_are_you_with_extra_info, self.explain_each_stat]
        self.obtained = {key: 0 for key in SIMPLE_PEEPS}
        self.history = []
        self.stat_desc = {
            "strength": "hit harder with melee attacks and pickup heavier objects.",
            "defense": "withstand harder hits and block better.",
            "evasion": "dodge attacks and move larger distances.",
            "dexterity": "hit targets accurately and craft items faster.",
            "recovery": "heal better and resist negative status effects.",
            "intelligence": "percieve hidden objects or routes and use spells.",
            "creativity": "make better items and food and invent new moves.",
            "fear": "resist scary enemies and situations before losing control.",
            "intimidation": "scare enemies and control others through aggression",
            "charisma": "persuade others and resist psychological effects.",
            "stress": "withstand situtations or activites that are hard work for longer.",
            "health": "take more damage before getting knocked out and improve regenerative effects upon self.",
            "hunger": "consume less food and resist stat debuffs.",
            "energy": "do more actions in combat and stay awake longer.",
        }

    def welcome(self):
        print(f"Welcome to the {self.name}!", 
              "\nHere you will choose a stat you value the most and the stat you value the least.",
              "Based on those choices, you will obtain a character that fits your preferences.",
              "Specifically, the given character will have the highest difference between your chosen stats.",
              "Before you get started, you can choose to play normally or with extra information detailing how the character was chosen.",)
        t.sleep(0.2)
    
    def who_are_you(self, verbose: bool = False):
        while True:
            
            most_choice = ""
            least_choice = ""

            #TODO: explain each stat and its purpose
            
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
                print("You chose: " + most_choice + " and " + least_choice)
                
            results = cdb.get_specific_combo_n_runner_ups(most_choice, least_choice)
            
            # check for ties.
            ties = []
            winning_diff = results[0]["diff"]
            
            for r in results[1:]:
                if r["diff"] == winning_diff:
                    ties.append(r["name"])
                else:
                    break
                
            
            winner = [p for p in SIMPLE_PEEPS if p.name == results[0]["name"]][0]
            
            # print sorted people
            if verbose:
                print("\nContenders: ")
                print(f"{'Name':<8}" + "Difference")
                for p in results:
                    name = p["name"]
                    print(f"{name:<7}" + ": " + str(p["diff"]))
                print()

            # TODO: perhaps only show the stats that the user chose?
            # FINAL ANSWER
            print("You got: " + str(winner))
            self.obtained[winner] += 1
            t.sleep(0.2)
            
            # communicate & store ties.
            if ties != []:
                print("You also could be...")
                for tie in ties:
                    peep = [p for p in SIMPLE_PEEPS if p.name == tie][0]
                    
                    # to print more peep info or not
                    if not verbose:
                        print(tie)
                    else:
                        print(peep)
                        
                    self.obtained[peep] += 1
                print()
            
            # log choices
            self.history.append((most_choice, least_choice, winner.name))
            
            # log ties
            if ties != []:
                for tie in ties:
                    self.history.append((most_choice, least_choice, tie))
            
            # print
            print("You have so far obtained:")
            for p in self.obtained:
                if self.obtained[p] == 0:
                    continue
                time_word_str = "times" if self.obtained[p] > 1 else "time"
                print(p.name + ": " + str(self.obtained[p]) + f" {time_word_str}!")
              
            # ask to play again or show history  
            continue_choice = 2      
            while continue_choice == 2:
                prompt = "Do you want to play again?"
                continue_choice = self.get_choice(
                ["Yes, continue", 
                 "No, return to menu", 
                 "Show history and decide after"], prompt=prompt)  
                
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
        
    def explain_each_stat(self):
        print("\nHere are the different stats and what they do: ")
        for stat in STAT_CHOICES:
            print(stat, "-",self.stat_desc[stat])
            
'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
'''   
            
class DistSimulator(Simulator):
    def __init__(self):
        self.name = "Distribution of Stat Combos Simulator"
        self.funcs = [self.view_combos_by_peep, 
                      self.view_combos_by_major_stat, 
                      self.view_combos_by_lesser_stat, 
                      self.view_count_of_combos_per_peep, 
                      ]
    
    def view_combos_by_peep(self):
        self.view_combos_by([p.name for p in SIMPLE_PEEPS], "name")
        
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
        t.sleep(0.2)    
        
'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
'''  

class StatManipulationSimulator(Simulator):
    def __init__(self):
        self.name = "Stat Manipulation Simulator"
        self.peeps = copy.deepcopy(PEEPS)
        self.funcs = [self.play_with_peep_stats, self.view_stats_of_all_peeps, self.play_with_equations] 
        
        self.peep_funcs = [self.manipulate_a_stat, self.manipulate_all_stats, 
                           self.compare_peep,
                           self.manage_every_alteration_on_peep, 
                           self.print_peep_info,
                           self.reset_peep_to_default]
        
        self.stat_funcs = [self.show_stat_info, self.grow_or_shrink_stat, 
                           self.set_stat_values_directly, self.manipulate_apt_level_by_xp,
                           self.manipulate_extra_modifiers, self.manage_stat_alterations,
                           self.reset_stat_to_default]
        
    def welcome(self):
        print(f"Welcome to the {self.name}!\n",
              "Here you can manually change the stats of a character to get a feel for",
              "how stat values are calcuated.",
              "You can also view a deep dive of different equations used for stat calcuations.") 
        t.sleep(0.2)      
    
    def view_stats_of_all_peeps(self):
        for peep in self.peeps:
            self.print_peep_info(peep)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    def play_with_peep_stats(self):
        while True:
            prompt = "Which peep would you like to do stat experimentation on?"
            peep = self.get_choice_with_exit(self.peeps, prompt=prompt)
            
            if peep is None:
                return
            
            # get user choice of peep func
            while True:
                prompt = f"What would you like to do with {peep.name}"
                peep_func = self.get_choice_with_exit(self.peep_funcs, prompt=prompt)
                
                if peep_func is None:
                    break
                
                peep_func(peep)
    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PEEP FUNCTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''        
    def print_peep_info(self, peep:BattlePeep):
        print(peep.get_info_as_str())
    
    def compare_peep(self, peep:BattlePeep):
        
        peeps_minus_this = copy.deepcopy(self.peeps)
        peeps_minus_this = [p for p in peeps_minus_this if p.name != peep.name]
        
        # get user choice of peep to compare
        while True:
            prompt = f"Who would you like to compare {peep.name} to?"
            comparer = self.get_choice_with_exit(peeps_minus_this, prompt=prompt)
            
            if comparer is None:
                break
            
            for stat_name in STAT_CHOICES:
                print(f"{peep.name}'s {stat_name}:", peep.get_stat(stat_name).print_simple_str())
                print(f"{comparer.name}'s {stat_name}:", comparer.get_stat(stat_name).print_simple_str())
                print()
            
    
    def reset_peep_to_default(self, peep:BattlePeep):
        print("\nPrevious Values: ")
        self.print_peep_info(peep)
        
        PeepManager.reset_peep_to_default(peep)
        
        print("\n--------------------------------------------------")
        print("Values after reset: ")
        self.print_peep_info(peep)
        
    
    def manage_every_alteration_on_peep(self, peep:BattlePeep):
        pass
    '''
        If any alterations:
        View all sorted by stat :)
        Choose a stat to modify alterations (call manage_stat_alterations)
        Delete all alterations on every stat :)
        
        Anytime:
        Create Alteration, but this time input stat to effect
        
    '''
    
    def delete_all_peep_alts(self, peep:BattlePeep):
        peep.stats.remove_all_alterations()
    
    def show_all_peep_alts(self, peep:BattlePeep):
        for stat in peep.stats.cur_stats.values():
            print(stat.name + ":" + stat.get_alt_info_as_str())
            print()
    
    def manipulate_all_stats(self, peep:BattlePeep):
        while True:
            # choose different funcs of manipulating the stat
            prompt = f"What would you like to do with all of {peep.name}'s stat?"
            chosen_func = self.get_choice_with_exit(self.stat_funcs, prompt=prompt) 
            
            if chosen_func is None:
                break
            
            for stat in peep.stats.cur_stats.values():
                chosen_func(peep, stat)     
    
    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~STAT MANIPULATION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    
    def manipulate_a_stat(self, peep:BattlePeep):
        
        while True:
            prompt = f"Which stat of {peep.name} would you like to manipulate"
            stat_name = self.get_choice_with_exit(STAT_CHOICES, prompt=prompt)
            
            if stat_name is None:
                return
            
            stat = peep.get_stat(stat_name)
            
            prompt = f"What would you like to do with the {stat_name} stat?"
            self.mini_sim(func_list=self.stat_funcs, args=[peep, stat], prompt=prompt)
    
       
    def set_stat_values_directly(self, peep:BattlePeep, stat:Stat):
        print("\nCurrent Values: ")
        print(stat.print_simple_str())
        
        print(f"Choose a new number for both the aptitude and the stat value.",
              'The aptitude must be between -4 and 8 (inclusive).')
        
        # input form
        change_in = { "apt": 0, "value": 0}
        conditions = [lambda x: x >= -4 and x <= 8, None]
        
        self.obtain_number_inputs(input_form_dict=change_in, conds=conditions)
        
        stat.set_new_vals(change_in['value'], change_in['apt'])
        
        print("\nWith Your Set Values: ")
        print(stat.print_simple_str())
        
    
    def grow_or_shrink_stat(self, peep:BattlePeep, stat:Stat):
        print("\nCurrent Values: ")
        print(stat.print_simple_str())
        
        # input form
        change_in = {"val_change": 0}
        conditions = [None]
        
        self.obtain_number_inputs(input_form_dict=change_in, conds=conditions)
        
        new_val = self.val + change_in['val_change']
        
        stat.set_new_vals(new_val, stat.apt)
        
        print("\nWith Your Set Values: ")
        print(stat.print_simple_str())
    
    def manipulate_apt_level_by_xp(self, peep:BattlePeep, stat:Stat):
        print("\nCurrent Stat Info: ")
        print(stat)
        
        # input form
        change_in = {"xp_change": 0}
        conditions = [None]
        
        self.obtain_number_inputs(input_form_dict=change_in, conds=conditions)
        
        stat.change_aptitude_xp(change_in['xp_change'])
        
        print("\nAfter your aptitude xp change: ")
        print(stat.print_simple_str())
    
    def show_stat_info(self, peep:BattlePeep, stat:Stat):
        print(stat, "\n")
        
    
    def manipulate_extra_modifiers(self, peep:BattlePeep, stat:Stat):
        pass
    
    def manage_stat_alterations(self, peep:BattlePeep, stat:Stat):
        print(f"Current alterations for {stat.name}: ")
        
        stat.get_alt_info_as_str()
        
        '''
            If any alterations:
            Delete All on stat
            
            Anytime:
            Create Alteration
                Choose preset
                Input values
        '''
        
        pass
    
    def reset_stat_to_default(self, peep:BattlePeep, stat:Stat):
        
        print("\nPrevious Values: ")
        print(stat)
        
        PeepManager.reset_stat_to_default(peep, stat)
        
        print("\nValues after reset: ")
        print(stat)
        print()
        
    
    '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EQUATIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''
    def play_with_equations(self):
        pass
       
    