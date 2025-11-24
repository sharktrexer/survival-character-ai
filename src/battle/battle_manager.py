import copy
import random
import time
from collections import namedtuple
from .battle_peep import BattlePeep, Peep_State, sn, GAUGE_STATS
from .battle_action import BattleAction #, basic_dmg, basic_heal, knife_stab, rat_chz

#temp_actions = [knife_stab, basic_heal, basic_dmg, rat_chz]

class MoveChoice:
    
    def __init__(self, move:BattleAction, target:BattlePeep, ap_spent:int):
        self.move = move
        self.target = target
        self.ap_spent = ap_spent
        
    def __repr__(self):
        return f"{self.move}, {self.target.name} target, {self.ap_spent} spent)"

class BattleManager():
    def __init__(self, members:list[BattlePeep]):
        self.rounds = 0
        self.members = members
        self.init_anchor = 0
        
    def get_anchor_init(self):
        # TODO: perhaps only call this when a change is calculated 
        """ 
        Sets the anchor initiative value to the lowest initiative value among the 
        peeps. The anchor value is used to determine when a peep gains 
        bonus AP. 
        
        The anchor should update when:
        1. The fight begins
        2. The end of a round (takes into account those who left, joined, knocked out)
        """
        if self.members == []: return 0
        
        valid_members = [peep for peep in self.members if not peep.stats.resource_is_depleted('hp')]
        if valid_members == []: return 0
        
        anchor = min(valid_members, key = lambda peep: peep.initiative())
        print("\nAnchor: " + anchor.name + " with init: " + str(anchor.initiative()))
        self.init_anchor = anchor.initiative()
    
    def get_member_names(self):
        return [peep.name for peep in self.members]
    
    def get_members_by_team(self, team:str, same_team:bool = True): 
        if same_team:
            return [peep for peep in self.members if peep.team == team]
        else:
            return [peep for peep in self.members if peep.team != team]
    
    def change_member_list(self, peep:BattlePeep, do_add:bool):
        if do_add:
            print("Added " + peep.name)
            self.members.append(peep)
        else:
            print("Removed " + peep.name)
            self.members.remove(peep)
        
        #self.get_anchor_init()
     
    def start_round(self):
        self.get_anchor_init()
        
        for peep in sorted(self.members, key = lambda peep: peep.initiative(), reverse=True):
            peep.start()
    
    def peep_start_turn(self, peep:BattlePeep, user_results:dict[str, int] = {}):

        # establish past peep data
        bd_start = BattleData(copy.deepcopy(peep), None)
        
        # calc growth if unit is alive
        if peep.points_of('hp') > 0: 
            self.do_gain_bonus_AP_from_init(peep)
        
        peep.start_turn()
        
        # grab changes
        bd_start.get_data_self(peep)
        
        # establish past knock down data
        bd_knocked = BattleData(copy.deepcopy(peep), None)
        
        peep.handle_knock_down()
        
        # grab changes
        bd_knocked.get_data_self(peep)
        
        # PRINT
        bd_start.print_self_changes(bd_knocked.user_b4, bd_start.user_diffs)
        bd_knocked.print_self_changes(peep, bd_knocked.user_diffs)
            
        peep.turns_passed += 1
        
        print()
        print(peep.get_label_as_str())
        

        
        
    
    def peep_action(self, peep:BattlePeep, move:MoveChoice):
        ''' Perform One Move '''
        move.move.cast(peep, move.target, move.ap_spent)
        peep.stats.resource_change('ap', -move.ap_spent)
        
        
        
    
    def peep_turn(self, peep:BattlePeep, moves:list[MoveChoice]):
        
        for cm in moves:
            self.peep_action(peep, cm)
            
        self.peep_end_turn(peep)
            
     
    def peep_end_turn(self, peep:BattlePeep):
        peep.end_turn()            
            
    def do_gain_bonus_AP_from_init(self, peep: BattlePeep):
        
        """
        Calculates whether a peep should gain bonus AP based on their initiative 
        relative to the anchor's initiative.

        Parameters:
            peep (BattlePeep): the peep to check
            anchor_init (int): the anchor's initiative

        Returns:
            bool: whether the peep gained bonus AP
        """
        past_growth = peep.init_growth
        peep.init_growth += max(0, peep.initiative() - self.init_anchor)
        # max is used so there is never negative growth
            
#~~~~~~~~ Dont show growth if there is none
        if peep.initiative() == self.init_anchor:
            #print(peep.name + " did not have growth as they are the anchor! :(")
            return False
#~~~~~~~~ Growth Calculation      
        else:         
            do_gain_bonus =  peep.init_growth >= 2 * self.init_anchor
            
            # print init growth
            #print(peep.name + " - Growth: " + str(past_growth) + " -> " + str(peep.init_growth))
            
            # let peep know they have bonus
            if do_gain_bonus:
                #print(peep.name + " - Gained energy bonus from initiative! Growth reset :O")
                peep.init_growth = 0
                peep.gained_ap_bonus = True
            
            return do_gain_bonus
    
    def get_action_affect(self, action:BattleAction, user:BattlePeep, target:BattlePeep, ap_used:int):
    # pass in copies!
    # use copy of battle manager!
    # simulate a cast on copies of user, target, action
    # see what has changed, status effects, alterations, healths, resources, summons
    # how much of each? was it positive or negative?
        
        user_past = copy.deepcopy(user)
        target_past = copy.deepcopy(target)
        
        bd = BattleData(user_past, target_past)
        
        self.peep_action(user, action)
        
        bd.get_data_target(user, target)
        
        user_results = {}
        target_results = bd.targ_diffs
        
        return bd
    
   
    
class BattleData():

        
    def __init__(self, past_user:BattlePeep, past_target:BattlePeep):
        '''  compare and store stats 4 easy access
        
        for user and target each: (and in future how it would affect everyone in battle!)
        
        get difference of all health (regular, evade, defense, blood, etc)
        
            get difference of resource values
            change of states
            get difference of alterations
            get difference of status effects
            was the action successful?
        
        '''
        self.user_b4 = past_user
        self.targ_b4 = past_target
        self.user_diffs: dict[str,int]  = {}
        self.user_chges: dict[str,BattleChange]  = {}
        self.targ_diffs: dict[str,int]  = {}
        self.targ_chges: dict[str,BattleChange] = {}
        
        pass
    
    def get_data_self(self, user:BattlePeep):
        self.user_diffs = BattleData.get_all_battle_resource_data(user, self.user_b4)
        self.user_chges['stance'] = BattleChange(new=user.stance(), old=self.user_b4.stance())
        
    
    def print_self_changes(self, user:BattlePeep, results:dict):
        
        if results[sn('ap')] != 0:
            print(f'{self.user_b4.points_of("ap")} -> {user.points_of('ap')} AP', end=" ")
        
        if user.stance() != self.user_b4.stance():
            print(f'({self.user_b4.stance()} -> {user.stance()})', end=" ")
        
        if results['dodge'] != 0:
            print(f'{self.user_b4.dodge()} -> {user.dodge()} Dodge', end=" ")
        
        if results['blood'] != 0:
            print(f'{self.user_b4.blood()} -> {user.blood()} Blood', end=" ")
        
        if user.stance() == Peep_State.DEAD and self.user_b4.stance() != Peep_State.DEAD:
            print(f'DIED!', end=" ")
            
    def get_data_target(self, user:BattlePeep, target:BattlePeep):
        
        t_res = BattleData.get_all_battle_resource_data(target, self.targ_b4)
        u_res = BattleData.get_all_battle_resource_data(user, self.user_b4)
        
        self.targ_chges['stance'] = BattleChange(new=target.stance(), old=self.targ_b4.stance())
        self.user_chges['stance'] = BattleChange(new=user.stance(), old=self.user_b4.stance())
        
        
        self.targ_diffs = t_res
        self.user_diffs = u_res
     
    @staticmethod     
    def get_all_battle_resource_data(p1:BattlePeep, p2:BattlePeep):
        info = {}
        
        # gauge stats
        for gs in GAUGE_STATS:
            info[gs] = BattleData.points_difference(p1, p2, gs)
        
        # battle health    
        for bh in ['armor', 'dodge', 'blood', 'temp']:
            info[bh] = BattleData.battle_health_difference(p1, p2, bh)
            
        return info
    
    @staticmethod    
    def points_difference(p1:BattlePeep, p2:BattlePeep, stat:str):
        return p1.points_of(stat) - p2.points_of(stat)

    @staticmethod    
    def battle_health_difference(p1:BattlePeep, p2:BattlePeep, type:str):
        health = None
        match(type):
            case 'dodge':
                health = p1.dodge() - p2.dodge()
            case 'blood':
                health = p1.blood() - p2.blood()
            case 'armor':
                health = p1.armor() - p2.armor()
            case 'temp':
                health = 0
            case _:
                raise ValueError(f'Invalid battle health type {type}')
        
        return health
        
        
BattleChange = namedtuple('Change', ['new', 'old'])
 