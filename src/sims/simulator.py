import visualization.graph_data as gd
import time as t

import peep_data.char_data as char_data

from abc import ABC, abstractmethod

from battle.intiative_sim import InitiativeSimulator 
from peep_data.char_data import STAT_TYPES, SIMPLE_PEOPLE, sort_peeps, get_highest_diff_peep

class Simulator(ABC):
    
    EXIT_KEY = "exit"
    
    name = 'DID NOT SET NAME'
    funcs = ['DID NOT SET FUNCS']
    
    @abstractmethod
    def simulate(self):
        pass
    
    @abstractmethod
    def welcome(self):
        pass
        
    def notify_of_option_to_exit(self):
        print(f"Enter {self.EXIT_KEY} to exit this simulation.")
    
    def validate_exit(self, user_in: str):
        return user_in.lower().strip() == self.EXIT_KEY
    
    def goodbye(self):
        print(f"Exiting {self.name}. Goodbye!")
        t.sleep(1)
    
    def choose_func(self):
        valid = False
        choice = ""
        
        while not valid:
            for i, s in enumerate(self.funcs):
                print(s.__name__, f"[{i+1}]")
                
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
    
    def simulate(self):
        print("\n")
            
        self.welcome()
        
        while True:
            exit_code = self.choose_func()
            if exit_code == 0:
                return
            t.sleep(1)



