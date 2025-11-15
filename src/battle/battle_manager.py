import copy
import random
import time
from .battle_peep import BattlePeep, Peep_State
from .battle_action import BattleAction #, basic_dmg, basic_heal, knife_stab, rat_chz
from .battle_ai import BattleAI, MoveChoice

#temp_actions = [knife_stab, basic_heal, basic_dmg, rat_chz]

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
        
    def next_round(self):
        self.rounds += 1
        
        print("\n~Round " + str(self.rounds) + "~")
        
        #print("\nCurrent Anchor Value: |" + str(self.init_anchor) + "|")
        #print("Target: |" + str(self.init_anchor*2) + "|")
        
        
        
        # order peep turns by initiative
        for peep in sorted(self.members, key = lambda peep: peep.initiative(), reverse=True):
            
            peep_copy = copy.deepcopy(peep)
            
            peep.turn()
            
            self_evade_decayed = peep_copy.battle_handler.evasion_health != peep.battle_handler.evasion_health
            
            if self_evade_decayed:
                print(f'{peep.name}: {peep_copy.battle_handler.evasion_health} -> {peep.battle_handler.evasion_health} EvaP', end=" ")
            
            peep.turns_passed += 1
            
            print()
            print(peep.get_label_as_str())
            
            # calc growth if unit is alive
            if not peep.stats.resource_is_depleted('hp'): 
                self.do_gain_bonus_AP_from_init(peep)
            else:
                continue
            
            peep_ai = BattleAI(peep)
            peep_ai.what_do(self.members)
            
            chosen_moves = peep_ai.choices
            
            ap_calc = peep_copy.stats.get_stat_resource('ap')
            
            for cm in chosen_moves:
                
                cur_move, chosen_targ = cm.move, cm.target
                
                target_name = chosen_targ.name
                
                print(f'({ap_calc} -> {ap_calc - cm.ap_spent} AP spent)', end=" ")
                
                #value = cur_move.get_value(peep.stats.get_stat_cur(cur_move.stat).val_active)
                if peep.name != target_name:
                    print(f'{peep.name} used {cur_move.name}' + f' on {target_name}', end=" ")
                else:
                    print(f'{peep.name} used {cur_move.name}', end=" ")
                
                ap_calc -= cm.ap_spent
                
                # get target by provided name
                target:BattlePeep = None
                for member in self.members:
                    if member.name == target_name:
                        target = member
                        break
                
                target_copy = copy.deepcopy(target)
                
                    
                # pass in ap spent if an ap flexible move was utilized
                
                cur_move.cast(peep, target, cm.ap_spent)
                
                affected_targ_hp = target.stats.get_stat_resource('hp') != target_copy.stats.get_stat_resource('hp')
                affected_targ_defAp = target.battle_handler.defense_health != target_copy.battle_handler.defense_health
                affected_targ_evaAp = target.battle_handler.evasion_health != target_copy.battle_handler.evasion_health
                affected_targ_bleed = target.battle_handler.bleed_out != target_copy.battle_handler.bleed_out
                
                # printing action effect
                if affected_targ_evaAp:
                    print(f'({target_copy.battle_handler.evasion_health} -> {target.battle_handler.evasion_health} EvaP)', end=" ")
                    
                if affected_targ_defAp:
                    print(f'({target_copy.battle_handler.defense_health} -> {target.battle_handler.defense_health} DefP)', end=" ")
                    
                if affected_targ_hp:
                    print(f'({target_copy.stats.get_stat_resource("hp")} -> {target.stats.get_stat_resource("hp")} HP)', end=" ")
                    
                if affected_targ_bleed:
                    print(f'({target_copy.battle_handler.bleed_out} -> {target.battle_handler.bleed_out} Bleed)', end=" ")
                print()
                
            
            peep.end_turn()
            print()
            time.sleep(0.01)
            
        # update anchor after round
        self.get_anchor_init()
            
            
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
    

   