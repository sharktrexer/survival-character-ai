import copy
from .battle_peep import BattlePeep, Damage
from .damage import create_dmg_preset, create_specific_phys_dmg
from .status_effects import StatusEffect
from .alteration import Alteration

class Behavior:
    '''
    Abstract class for behaviors
    '''
    def __init__(self, for_self:bool = False):
        self.for_self = for_self
    
    def execute(self, user:BattlePeep, target:BattlePeep):
        '''
        Sets target to user if this behavior is for self
        
        Doesn't do anything else
        '''
        if self.for_self:
            target = user
    
    
class DealDamage(Behavior):
    def __init__(self, damage:Damage, for_self:bool = False):
        super().__init__(for_self)
        self.damage = damage
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        super().execute(user, target)
        
        self.damage.give_value(user.stats.get_stat_active(self.damage.empowering_stat))
        
        target.affect_hp(self.damage)
        
        self.damage.amount = 0
        
class AugmentDamage(Behavior):
    def __init__(self, damage:Damage, for_self:bool = False):
        super().__init__(for_self)
        self.damage = damage
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        # reset previous give value
        self.damage.amount = 0
        
        super().execute(user, target)
        
        self.damage.give_value(user.stats.get_stat_active(self.damage.empowering_stat))
        
        print(f"Augment: {self.damage.amount} ({self.damage.ratio}/{self.damage.empowering_stat})",
              end=' ')

class ChangeState(Behavior):
    def __init__(self, state, for_self:bool = False):
        super().__init__(for_self)
        
        self.state = state
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        super().execute(user, target)
        
        target.change_state(self.state)
 
class Condition(Behavior):
    def __init__(self, is_and:bool = False, for_self:bool = False):
        super().__init__(for_self)
        
        self.AND = is_and # this condition and the previous conditions must be met
        self.met = False
        
        '''
        Accept special language for conditions
        
        Knockdown example:
            condition = user str * 1.5 > (targ current HP / 2) + targ current health ratio * targ Def
                = u.str * 1.5 > t.cur_hp / 2 + t.hp_ratio * t.def
            condition = user dex > targ current health ratio * targ Eva + (targ evade health / 4)
                = u.dex > t.hp_ratio * t.eva + (t.eva_hp / 4)
        '''
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        super().execute(user, target)
        
class KnockDown(Behavior):
    '''
    Break down into
    Condition
    Effect
    Condition
    Effect
    '''
    def __init__(self, for_self:bool = False):
        super().__init__(for_self)
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        '''
        Knocks down target if:
        1.5x STR to be more than target's (current HP / 2) + current health ratio * Def
        Dex to be greater than target's current health ratio * EVA + (Evade Health / 4)
        '''
        super().execute(user, target)        
        
        strength = user.stats.get_stat_active("str") * 1.5
        dex = user.stats.get_stat_active("dex")
        
        targ_cur_hp = target.stats.get_stat_resource("hp") // 2
        targ_hp_ratio = target.stats.get_stat_resource("hp") // target.stats.get_stat_active("hp")
        targ_def = target.stats.get_stat_active("def") * targ_hp_ratio
        targ_eva = target.stats.get_stat_active("eva") * targ_hp_ratio
        targ_eva_hp = target.battle_handler.evasion_health // 4
        
        dex_success = dex > targ_eva + targ_eva_hp
        str_success = strength > targ_cur_hp + targ_def

class CheckEvade(Behavior):
    '''
    Used to check if the target would evade whatever has this behavior
    Automatically applied to the start of the behaviors list of an action that uses DealDamage
    '''
    def __init__(self):
        self.for_self = False
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        '''
        Returns if target used evasion health to evade attack
        '''
        super().execute(user, target)
        
        return target.try_to_evade(user)
        
class GainEvasion(Behavior):
    '''
    Target gains evasion health based on their EVA x passed in multiplier 
    '''
    def __init__(self, eva_mult, for_self:bool = False):
        super().__init__(for_self)    
        self.eva_mult = eva_mult
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        super().execute(user, target)
        
        amount = target.stats.get_stat_active("eva") * self.eva_mult
        
        target.change_evasion_health(amount)
        
     
class ApplyStatusEfct(Behavior):
    def __init__(self, stat_effect:StatusEffect, for_self:bool = False):
        super().__init__(for_self)
        self.stat_effect = stat_effect
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        super().execute(user, target)
        
        target.status_effects.append(self.stat_effect)
        

class ApplyAlteration(Behavior):
    def __init__(self, alteration:Alteration, for_self:bool = False):
        super().__init__(for_self)
        self.alteration = alteration        
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        super().execute(user, target)
        target.recieve_alt(self.alteration)
        
class BattleAction():
    def __init__(self, name:str, ap_cost:int, behaviors:list[Behavior]):
        self.name = name
        self.ap = ap_cost
        self.flexible = self.get_ap_flexibility()
        self.behaviors = behaviors
        self.evadable = False
        
        # check that AugmentDamage(s) come before DealDamage  
        # also while we're checking, if there is a DealDamage then this action is evadable      
        auging = False
        for behavior in self.behaviors:
            if isinstance(behavior, AugmentDamage):
                auging = True
            elif isinstance(behavior, DealDamage):
                auging = False
                self.evadable = True
                self.behaviors.insert(0, CheckEvade())
            elif auging:
                break
            
        if auging:
            raise Exception(
                ("AugmentDamage(s) must come before DealDamage and"
                + " there must be a DealDamage after AugmentDamage(s)")
                )
        
        # temporary modification of an action's behavior
        # Example: an electric glove may add a 0.1 of int DealDamage behavior to an action    
        self.behaviors_modified = copy.deepcopy(self.behaviors)
        
        self.action_type = self.get_action_type()
    
    def get_ap_flexibility(self):
        if self.ap_cost < 0:
            return True
        return False
                
    def reset_behaviors(self):
            self.behaviors_modified = copy.deepcopy(self.behaviors)
    
    # TODO: account for non damage dealing behaviors
    def get_action_type(self):
        for behavior in self.behaviors_modified:
            if isinstance(behavior, DealDamage):
                if behavior.damage.is_heal:
                    return "heal"
                return "dmg"
        
    def cast(self, user:BattlePeep, target:BattlePeep):
        
        auged_dmg = 0
        
        # TODO: if ap flexible, cast for as many times as Ap used
        for behavior in self.behaviors_modified:
            
            # check if the target would evade this attack
            if isinstance(behavior, CheckEvade):
                # stop cast if evaded
                if behavior.execute(user, target):
                    return
            
            # grab extra damage to add to final attack
            if isinstance(behavior, AugmentDamage):
                behavior.execute(user, target)
                auged_dmg += behavior.damage.amount
                continue
            
            # add aug dmg to DealDamage behavior   
            if auged_dmg != 0 and isinstance(behavior, DealDamage):
                behavior.damage.amount = auged_dmg
                auged_dmg = 0
                
            behavior.execute(user, target)
            
    def cast_aoe(self, user:BattlePeep, targets:list[BattlePeep]):
        # TODO: raise error if this is not an aoe move
        # TODO: check for self_only behaviors and only apply them once instead of for every target
        for target in targets:
            self.cast(user, target)
            
    def get_damage_per_stat(self) -> dict[str, float]:
        '''
        Returns a dictionary of stat name to damage ratio
        based on the damage behaviors
        
        Assumes that the functionalaity of AugmentDamage's {is_heal} variable opposing the 
        DealDamage's {is_heal} variable means the Augment decreases the damage instead of increasing
        
        Utlized by the in game AI to make the best move decision when taking in account
        their BattlePeep obj stats
        
        EXAMPLE:
            An enemy with high Strength and Dexterity may usually choose
            between 2 different actions that deal 0.8x of either stat.
            
            If they recieve a negative Strength augment of 0.1, then the Dexterity
            action will have a higher likelyhood of being chosen
        
        '''
        
        stat_2_dmg_dict = {}
        is_heal = False
        
        for behavior in reversed(self.behaviors_modified):
            
            # grab the action's main damage source
            if isinstance(behavior, DealDamage):
                
                # check if healing. Any augments that are opposing this value
                # count as decreasing the damage ratio
                is_heal = behavior.damage.is_heal
                
                if behavior.damage.empowering_stat not in stat_2_dmg_dict:
                    stat_2_dmg_dict[behavior.damage.empowering_stat] = 0 # initialize key
                    
                stat_2_dmg_dict[behavior.damage.empowering_stat] += behavior.damage.ratio
            
            # check the augments    
            elif isinstance(behavior, AugmentDamage):
                
                if behavior.damage.empowering_stat not in stat_2_dmg_dict:
                    stat_2_dmg_dict[behavior.damage.empowering_stat] = 0 # initialize key
                
                # if opposing the DealDamage's goal, reduce the ratio
                if is_heal != behavior.damage.is_heal:
                    stat_2_dmg_dict[behavior.damage.empowering_stat] -= behavior.damage.ratio
                else:
                    stat_2_dmg_dict[behavior.damage.empowering_stat] += behavior.damage.ratio
            else:
                continue
                
        return stat_2_dmg_dict
        

basic_heal = BattleAction("Heal",[
    DealDamage(create_dmg_preset(0.8, Damage.DamageType.Healing))
])

basic_dmg = BattleAction("Attack",[
    DealDamage(create_dmg_preset(0.6, Damage.DamageType.Physical))
])
            
rat_chz = BattleAction("Cheese Plate",[
    DealDamage(create_dmg_preset(0.3, Damage.DamageType.Healing), for_self=True),
    DealDamage(create_dmg_preset(0.8, Damage.DamageType.Healing))
])

knife_stab = BattleAction("Knife Stab",[
    AugmentDamage(create_specific_phys_dmg(0.8, 'dex')),
    AugmentDamage(create_specific_phys_dmg(0.1, 'int')),
    DealDamage(create_dmg_preset(0.2, Damage.DamageType.Physical)),
])



