import copy
from sims.simulator import Simulator
from collections import defaultdict

from battle.battle_manager import BattleManager
from battle.battle_peep import BattlePeep, Attack
from battle.stats import Stat, make_stat

from peep_data.data_reader import PEEPS

import time as t

# TODO: put into its own file
TEMP_ENEMIES = [
    BattlePeep("Rat", {
        "strength": make_stat("str", 10, -2),
        "defense": make_stat("def", 10, 0),
        "evasion": make_stat("eva", 20, 4),
        "dexterity": make_stat("dex", 15, 2),
        "recovery": make_stat("rec", 10, 0),
        "intelligence": make_stat("int", 10, -1),
        "creativity": make_stat("cre", 8, -4,),
        "fear": make_stat("fear", 10, 0),
        "intimidation": make_stat("itmd", 10, -1),
        "charisma": make_stat("cha", 8, -2,),
        "stress": make_stat("tres", 10, 0),
        "health": make_stat("hp", 40, 0),
        "hunger": make_stat("hun", 20, -1),
        "energy": make_stat("ap", 8, 0),
    }),
    BattlePeep("Double Rat", {
        "strength": make_stat("str", 20, 0),
        "defense": make_stat("def", 10, 2),
        "evasion": make_stat("eva", 15, 2),
        "dexterity": make_stat("dex", 20, 2),
        "recovery": make_stat("rec", 10, 1),
        "intelligence": make_stat("int", 15, -1),
        "creativity": make_stat("cre", 10, -3,),
        "fear": make_stat("fear", 15, 1),
        "intimidation": make_stat("itmd", 10, 1),
        "charisma": make_stat("cha", 12, -2,),
        "stress": make_stat("tres", 10, -2),
        "health": make_stat("hp", 80, 1),
        "hunger": make_stat("hun", 20, -2),
        "energy": make_stat("ap", 10, 1),
    }),
    BattlePeep("Heavy Slime", {
        "strength": make_stat("str", 20, 2),
        "defense": make_stat("def", 20, 4),
        "evasion": make_stat("eva", 4, -3),
        "dexterity": make_stat("dex", 4, -3),
        "recovery": make_stat("rec", 10, 0),
        "intelligence": make_stat("int", 5, -4),
        "creativity": make_stat("cre", 5, -3,),
        "fear": make_stat("fear", 30, 3),
        "intimidation": make_stat("itmd", 10, 0),
        "charisma": make_stat("cha", 5, -4,),
        "stress": make_stat("tres", 50, 8),
        "health": make_stat("hp", 100, 4),
        "hunger": make_stat("hun", 20, 0),
        "energy": make_stat("ap", 10, 0),
    }),
    BattlePeep("Ent", {
        "strength": make_stat("str", 10, 2),
        "defense": make_stat("def", 20, 4),
        "evasion": make_stat("eva", 10, 0),
        "dexterity": make_stat("dex", 15, 1),
        "recovery": make_stat("rec", 20, 4),
        "intelligence": make_stat("int", 15, 3),
        "creativity": make_stat("cre", 10, 2,),
        "fear": make_stat("fear", 15, 2),
        "intimidation": make_stat("itmd", 10, -1),
        "charisma": make_stat("cha", 10, 0,),
        "stress": make_stat("tres", 20, 4),
        "health": make_stat("hp", 133, 3),
        "hunger": make_stat("hun", 20, 4),
        "energy": make_stat("ap", 8, 2),
    }),
    
]

def set_teams():
    for peep in PEEPS:
        peep.team = "peep"
    for peep in TEMP_ENEMIES:
        peep.team = "enemy"
        
set_teams()

test_attack = Attack(name="Attack", associated_stat_name="Strength", 
                     percent_of_stat_2_value=0.8)
test_heal = Attack(name="Heal", associated_stat_name="Recovery",
                   is_for_team=True, 
                   is_heal=True,
                   percent_of_stat_2_value=0.5)

PLAYGROUND = PEEPS + TEMP_ENEMIES

VALID_NAMES = [p.name for p in PLAYGROUND]

peep_test_group = PEEPS[0:3]

def give_battle_peeps_moves():
    for peep in PLAYGROUND:
        peep.move_set.append(test_attack)
        peep.move_set.append(test_heal)
        
give_battle_peeps_moves()

peep_copy_tracker = defaultdict(int)

class BattleSimulator(Simulator):
    def __init__(self):
        self.name = "Battle Simulator"
        self.funcs = [self.next_round,
                      self.modify_battle,
                      self.print_current_peeps, 
                      self.print_spawn_options, 
                      self.reset_battle,
                      self.manage_debug_info,
                      ]
                      
        self.battler = BattleManager([])
        
        # TODO: turn into own class to manage toggles of all debugs
        # this will allow different print statements throughout battle based on these choices
        self.show_init_debug = False
        self.show_alt_debug = False
        self.debug_mode = False

        
    def welcome(self):
        print(f"Welcome to the {self.name}!\n", 
              "Here you can simulate a battle between characters.",
              "There are many different things to do so have fun!")
        t.sleep(0.2)
        #TODO: get input of who the player wants to be
        
    def toggle_init_debug(self):
        self.show_init_debug = not self.show_init_debug
        
    def toggle_alt_debug(self):
        self.show_alt_debug = not self.show_alt_debug
        
    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        self.show_alt_debug = self.debug_mode
        self.show_init_debug = self.debug_mode
        
    def manage_debug_info(self):
        pass
        
    def modify_battle(self):
        
        if self.battler.members != []:
            print("Add or remove something?")
            do_add = bool(self.get_choice(["Remove", "Add"]))
            verb_str = "Add" if do_add else "Remove"
        else:
            # no need to ask to remove if there are no peeps
            do_add = True
            verb_str = "Add"
        
        #TODO: choices should have more info on char, like init, etc
        choices = VALID_NAMES if do_add else self.battler.get_member_names()
            
        if not choices:
            print("No members to remove.")
            return
        
        choices.append(self.EXIT_KEY)
        
        # loop to allow multiple removals or additions
        while True:
            
            # if only the option to exit remains, break out
            if len(choices) == 1:
                print("No members to remove.")
                return
            
            print(f"Choose what to {verb_str}:")
            peep_name = choices[self.get_choice(choices)]
            
            # exit option
            if peep_name == self.EXIT_KEY:
                return
            
            # get peep by name
            peep = [p for p in PLAYGROUND if p.name == peep_name][0]
            
            # give peep new name to differentiate it between copies
            if do_add:
                peep = copy.deepcopy(peep)
                suffix = "" if peep_copy_tracker[peep.name] == 0 else f" {peep_copy_tracker[peep.name]}"
                peep_copy_tracker[peep.name] += 1
                peep.name = f"{peep.name}{suffix}"
                
                
            self.battler.change_member_list(peep, do_add)
            
            
            # ensure updated list when removing
            if not do_add:
                choices.remove(peep_name)
            
            print(f"\n{verb_str} more!")
            t.sleep(0.2)
            

    def print_current_peeps(self):
        print("~Members~")
        if not self.battler.members:
            print("None")
            return
        for p in self.battler.members:
            print("[",p.name, "] with init: ", str(p.initiative()))
            
    def print_spawn_options(self):
        print("~Spawnables~")
        for p in PLAYGROUND:
            print("[",p.name, "] with init: ", str(p.initiative()))
            
    def next_round(self):
        
        if self.check_if_no_peeps():
            return
        
        if self.battler.rounds == 0:
            self.battler.start_round()
        
        self.battler.next_round()
        
    def reset_battle(self):
        if self.check_if_no_peeps():
            return
        print("Resetting Battle...")
        self.battler = BattleManager([])
        
    def check_if_no_peeps(self):
        '''
        The Battle Manager works without containing members, but this simulator
        should be able to communicate that to the user and pass calling
        functions that would do nothing without peeps.
        
        Returns:
            bool: if there are peeps in the battle
        '''
        no_peeps = self.battler.members == []
        if no_peeps:
            print("\nThere is no one here so nothing happened...",
                  "You should add some peeps using the modify battle option.")
        return no_peeps
    
    def choose_player(self):
        pass
        

'''
class InitiativeSimulator(BattleSimulator):
    def __init__(self):
        self.name = "Initiative Simulator"
        self.funcs = []
        
    def start_round(self):
        super().start_round()
        
        print("~Intiative Sim~", "\n")
        print("Members:")
        for p in self.init_tester.members:
            
            print("[",p.name, "] with init: ", str(p.initiative()), sep="")
        
'''