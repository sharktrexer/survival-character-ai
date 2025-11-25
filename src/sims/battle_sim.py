import copy
from battle.alteration import AP_BUFF
from sims.simulator import Simulator
from collections import defaultdict

from battle.battle_manager import BattleData, BattleManager, MoveChoice, BattleAction
from battle.battle_peep import BattlePeep, Peep_State as state
from battle.stats import Stat, make_stat
from battle.peep_manager import PeepManager
from battle.battle_ai import BattleAI, simulate

from peep_data.data_reader import PEEPS

import time as t

# TODO: put into its own file
TEMP_ENEMIES = [
    BattlePeep("Rat", {
        "strength": make_stat("str", 10, -2),
        "defense": make_stat("def", 5, 0),
        "evasion": make_stat("eva", 20, 4),
        "dexterity": make_stat("dex", 15, 2),
        "recovery": make_stat("rec", 10, 0),
        "intelligence": make_stat("int", 10, 2),
        "creativity": make_stat("cre", 8, -2,),
        "fear": make_stat("fear", 10, 0),
        "intimidation": make_stat("itmd", 10, -1),
        "charisma": make_stat("cha", 8, -2,),
        "stress": make_stat("tres", 10, 0),
        "health": make_stat("hp", 40, 0),
        "hunger": make_stat("hun", 20, -1),
        "energy": make_stat("ap", 8, 0),
    }),
    BattlePeep("Double_Rat", {
        "strength": make_stat("str", 10, 0),
        "defense": make_stat("def", 10, 2),
        "evasion": make_stat("eva", 15, 2),
        "dexterity": make_stat("dex", 15, 0),
        "recovery": make_stat("rec", 10, 1),
        "intelligence": make_stat("int", 20, -1),
        "creativity": make_stat("cre", 10, -3,),
        "fear": make_stat("fear", 15, 1),
        "intimidation": make_stat("itmd", 10, 1),
        "charisma": make_stat("cha", 16, -2,),
        "stress": make_stat("tres", 10, -2),
        "health": make_stat("hp", 70, 1),
        "hunger": make_stat("hun", 20, -4),
        "energy": make_stat("ap", 10, 1),
    }),
    BattlePeep("Heavy_Slime", {
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
        "health": make_stat("hp", 40, 0),
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

PLAYGROUND = PEEPS + TEMP_ENEMIES

VALID_NAMES = [p.name for p in PLAYGROUND]

peep_test_group = PEEPS[0:3]

peep_copy_tracker = defaultdict(int)

class BattleSimulator(Simulator):
    def __init__(self):
        self.name = "Battle Simulator"
        self.funcs = [self.next_round,
                      self.modify_battle,
                      self.simulate_multiple_rounds,
                      self.print_current_peeps, 
                      self.print_spawn_options, 
                      self.reset_battle,
                      self.bleed_out_peep
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
        choices = copy.deepcopy(VALID_NAMES) if do_add else self.battler.get_member_names()
            
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
                
                peep.is_player = bool(self.get_choice(["No", "Yes"], prompt=f"Do you want to manually control {peep.name}?"))
                
                
            self.battler.change_member_list(peep, do_add)
            
            
            # ensure updated list when removing
            if not do_add:
                choices.remove(peep_name)
            
            print(f"\n{verb_str} more!")
            t.sleep(0.01)
            

    def print_current_peeps(self):
        print("~Members~")
        if not self.battler.members:
            print("None")
            return
        
        for p in self.battler.members:
            print(f"[{p.get_label_as_str()}] with init: ", str(p.initiative()))
            
    def print_spawn_options(self):
        print("~Spawnables~")
        for p in PLAYGROUND:
            print("[",p.name, "] with init: ", str(p.initiative()))
            
    def next_round(self):
        
        if self.check_if_no_peeps():
            return
        
        if self.battler.rounds == 0:
            self.battler.start_round()
        
        self.battler.rounds += 1
        
        print("\n~Round " + str(self.battler.rounds) + "~")
        
        # members by initiative
        for peep in sorted(self.battler.members, key = lambda peep: peep.initiative(), reverse=True):
            
            # start turn
            self.battler.peep_start_turn(peep)
            
            if AP_BUFF in peep.stats.get_stat_cur('ap').buffs:
                print(f'Gained AP BUFF due to initiative!')

            # player or AI moves or no moves
            if peep.stance() == state.DEAD or peep.stance() == state.BLEEDING_OUT:
                moves = []
            elif peep.is_player:  
                moves = self.get_player_moves(peep)
            else:
                peep_brain = BattleAI(peep)
                dirty_moves = simulate(peep_brain, copy.deepcopy(self.battler))
                moves = [move.move for move in dirty_moves]
                #peep_brain.what_do(self.battler.members)
                #moves = peep_brain.choices
            
            
            ''' Action Loop'''
            for ac in moves:
        
                # !BATTLEDATA!
                target = self.battler.get_peep_by_name(ac.target)
                bd = BattleData(copy.deepcopy(peep), copy.deepcopy(target))
                
                
                ''' THE BIG CAST '''
                self.battler.peep_action(peep, ac)
                ''' THE BIG CAST '''
                
                
                bd.get_data_target(peep, target)
                
                peep_results = bd.user_diffs
                targ_diffs = bd.targ_diffs
                targ_changes = bd.targ_chges
                
                ''' Obtain What the move did to the target '''
                # ap usage info
                print(f'({bd.user_b4.points_of("ap")} -> {peep.points_of("ap")} AP spent)', end=" ") 
                
                # basic action info
                if peep.name != target.name:
                    print(f'{peep.name} used {ac.move.name}' + f' on {target.name}', end=" ")
                else:
                    print(f'{peep.name} used {ac.move.name}', end=" ")  
                
                
                # printing action effect
                if targ_diffs['dodge'] != 0:
                    print(f'({bd.targ_b4.dodge()} -> {target.dodge()} Dodge)', end=" ")
                    
                if targ_diffs['armor'] != 0:
                    print(f'({bd.targ_b4.armor()} -> {target.armor()} Armor)', end=" ")
                    
                if targ_diffs['health'] != 0:
                    print(f'({bd.targ_b4.points_of("hp")} -> {target.points_of("hp")} HP)', end=" ")
                
                if targ_changes['stance'].new != targ_changes['stance'].old:
                    print(f'({bd.targ_b4.stance()} -> {target.stance()})', end=" ")
                    
                if targ_diffs['blood'] != 0:
                    print(f'({bd.targ_b4.blood()} -> {target.blood()} Bleed)', end=" ")
                print()
            
            # END TURN
            self.battler.peep_end_turn(peep)   
            print()
            t.sleep(0.01)
        
        # update anchor after round    
        self.battler.get_anchor_init()
    
    ''' TODO: option to choose 
    OFFENSIVE (attacks, gauge attacks, debuff, negative status) 
    DEFENSIVE (defends, heal, gauge heal, buff, positive status)
    ACTION [affects objs or envrionment] 
        (Barricade, Perceive, Interact, Shove, Throw, Pick Up, Summon, Cover Face, Cover Ears)
    SOCIAL (Alert, suggest, command, bargain)
    '''
    def get_player_moves(self, peep:BattlePeep):
        peep_move_state = BattleAI(peep)
        
        while peep_move_state.can_still_cast:
            
            completed_move = MoveChoice(None, None, 0)
            
            ''' Get Move Choice'''
            prompt = f"Choose a move for {peep.name} | {peep_move_state.my_ap}/{peep.value_of("ap")} AP | {len(peep_move_state.choices)}/3 Moves Used:"
            action_choice:BattleAction = self.get_choice_with_exit(peep_move_state.moves, prompt=prompt)
            if action_choice == None:
                return peep_move_state.choices
            
            completed_move.move = action_choice
            
            ''' Get Flexibility Ap Usage'''
            if action_choice.flexible:
                num_of_uses = peep_move_state.my_ap // action_choice.ap
                
                desired = {'uses':0}
                cond = [lambda x: x >= 1 and x <= num_of_uses]
                
                print(f"How many times would you like to use {action_choice.name}?",
                      f"The number of uses must be between 1 and {num_of_uses} (inclusive).")
                self.obtain_number_inputs(input_form_dict=desired, conds=cond)
                
                completed_move.ap_spent = action_choice.ap * int(desired['uses'])
                
            ''' Get Target '''
            if action_choice.for_self_only:
                completed_move.target = peep.name
            else:
                #TODO: if no valid allies, then don't provide ally only moves!
                # get enemies or allies based on move
                get_same_team = action_choice.action_type == "heal"
                prompt = f"Choose a target for {action_choice.name}:"
                valid_targs = self.battler.get_members_by_team(peep.team, get_same_team)
                targ_choice_ind = self.get_choice(choices=valid_targs, prompt=prompt)
                target_choice = valid_targs[targ_choice_ind]
                
                completed_move.target = target_choice.name
            
            ''' Get Ap Spent If Not Flexible'''    
            if completed_move.ap_spent == 0:
                completed_move.ap_spent = action_choice.ap
                
            peep_move_state.update_peep_move_state(completed_move)
            
        return peep_move_state.choices
            
        
    def simulate_multiple_rounds(self):
        
        if self.check_if_no_peeps():
            return
        
        prpmt = "Would you like to simulate rounds fast?"
        bool_fast = self.get_choice(["No", "Yes"], prompt=prpmt)
        
        number_of = {"rounds": 0}
        conditions = [lambda x: x >= 2]
        
        print("How many rounds would you like to simulate?")
        self.obtain_number_inputs(input_form_dict=number_of, conds=conditions)
        
        number_of['rounds'] = int(number_of['rounds'])
        
        for i in range(number_of['rounds']):
            self.next_round()
            if bool_fast:
                t.sleep(0.1)
            else:
                input("Enter to continue...")
            
        
    def bleed_out_peep(self):
        choice = self.get_choice_with_exit(self.battler.members)
        
        if choice is None:
            return
        
        for m in self.battler.members:
            if m.name == choice.name:
                choice = m
        
        PeepManager.kill_peep(choice)    
        
        
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