import copy
from enum import Enum, auto
from typing import Callable
from .battle_peep import BattlePeep, Damage, Peep_State
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
        The core of behavior logic
        '''
        if self.for_self:
            return user
        return target
    
    def __repr__(self):
        return f"{self.__class__.__name__}"

class FlexibleAPBehavior(Behavior):
    '''
    Inherit from this class to behave differently given ap value
    '''
    def __init__(self,for_self:bool = False):
        super().__init__(for_self)
        
    def execute(self, user:BattlePeep, target:BattlePeep, ap:int):
        return super().execute(user, target)
    
class DealDamage(Behavior):
    def __init__(self, damage:Damage, for_self:bool = False):
        super().__init__(for_self)
        self.damage = damage
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        target = super().execute(user, target)
        
        self.damage.give_value(user.stats.get_stat_active(self.damage.empowering_stat))
        
        # print(f"HIT: {self.damage.amount} (+{self.damage.ratio}/{self.damage.empowering_stat})",
        #       end=' ')
        
        target.affect_hp(self.damage)
        
        self.damage.amount = 0
        self.damage.mult = 1.0
        
        
class AugmentDamage(Behavior):
    '''
    Comes before a DealDamage to augment the damage value
    
    Used to apply extra damage to an attack through addition than a separate damage attempt
    
    Inserting into lists will be done before the first DealDamage
    '''
    def __init__(self, damage:Damage, for_self:bool = False):
        super().__init__(for_self)
        self.damage = damage
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        # reset previous give value
        self.damage.amount = 0
        
        target = super().execute(user, target)
        
        self.damage.give_value(user.stats.get_stat_active(self.damage.empowering_stat))
        
        # print(f"Augment: {self.damage.amount} ({self.damage.ratio}/{self.damage.empowering_stat})",
        #       end=' ')
        
        self.damage.mult = 1.0

class ChangeState(Behavior):
    def __init__(self, state:Peep_State, for_self:bool = False):
        super().__init__(for_self)
        
        self.state = state
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        target = super().execute(user, target)
        
        target.change_state(self.state)

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
        
        return target.try_to_evade(user)
        
class GainEvasionHealth(FlexibleAPBehavior):
    '''
    Target gains evasion health based on their EVA x passed in multiplier 
    '''
    def __init__(self, eva_mult, for_self:bool = False):
        super().__init__(for_self)    
        self.eva_mult = eva_mult
        
    def execute(self, user:BattlePeep, target:BattlePeep, ap:int):
        target = super().execute(user, target, ap)
        
        amount = int(round(target.stats.get_stat_active("eva") * self.eva_mult)) * ap
        
        #print(f"EVA Health: +{amount}")
        
        target.change_evasion_health(amount)
        
class GainDefenseHealth(FlexibleAPBehavior):
    '''
    Target gains evasion health based on their EVA x passed in multiplier 
    '''
    def __init__(self, def_mult, for_self:bool = False):
        super().__init__(for_self)    
        self.def_mult = def_mult
        
    def execute(self, user:BattlePeep, target:BattlePeep, ap:int):
        target = super().execute(user, target, ap)
        
        amount = int(round(target.stats.get_stat_active("def") * self.def_mult)) * ap
        
        #print(f"DEF Health: +{amount}")
        
        target.change_defense_health(amount)

class ReduceEvasionHealth(Behavior):
    def __init__(self, percent:float, for_self:bool = False):
        super().__init__(for_self)
        self.percent = percent
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        target = super().execute(user, target)
        
        eva_hp = target.battle_handler.evasion_health
        
        target.change_evasion_health(-int(eva_hp * self.percent))
     
class ApplyStatusEfct(Behavior):
    def __init__(self, stat_effect:StatusEffect, for_self:bool = False):
        super().__init__(for_self)
        self.stat_effect = stat_effect
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        target = super().execute(user, target)
        
        target.status_effects.append(self.stat_effect)
        

class ApplyAlteration(Behavior):
    def __init__(self, alteration:Alteration, for_self:bool = False):
        super().__init__(for_self)
        self.alteration = alteration        
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        target = super().execute(user, target)
        target.recieve_alt(self.alteration)

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Conditions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~''' 
 
class Condition(Behavior):
    '''
    Stores a function that uses self and target to provide condition logic
    If true is returned, the next behaviors are executed until another condition changes boolean
    Otherwise, ignore all non-condition behaviors until next condition behavior
    
    Multiple Conditions can be built upon one another to create a more complex one
        AND = True if you want stacking conditions, or AND = False if you want any
        one of the conditions to be met. Mix and match as desired
        
        
        Remember: more conditions doesn't equal more fun
    '''
    def __init__(self, cond_func:Callable[[BattlePeep, BattlePeep],bool], AND:bool = False):
        self.cond_func = cond_func  
        
        self.met = False
        
        self.AND = AND # if true, previous condition must also be met
        
        self.cur_cond = True 
        # what the current state of the condition is on action
        # set when batle action finds this in list
        
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        return self.cond_func(user, target)
    
class ReverseCondition(Condition):
    '''
    Assumes self.cur_cond is already set
    
    Will return the opposite of cur_cond
    '''
    def __init__(self):
        self.cond_func = None
        
    def execute(self, user, target):
        return not self.cur_cond

class YesCondition(Condition):
    '''
    Always returns True
    
    Useful for adding behaviors to the end of the action without 
    worrying about previous conditions
    '''
    def __init__(self):
        self.cond_func = None
        self.AND = False
        
    def execute(self, user, target):
        return True

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Flags ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~''' 

class Flag(Behavior):
    '''
    Used to flag hard coded decisions a battle action may make
    
    No functionality otherwise
    
    Helpful for working with Conditions
    '''
    def __init__(self):
        self.flag = True
        
    def execute(self, user, target):
        return
    
class ABORT(Flag):
    '''
    Used to cancel an action.
    All conditions before it will be executed
    All conditions after will not
    '''
    def __init__(self):
        super().__init__()
        
class UNEVADABLE(Flag):
    '''
    Marks an action as unevadable, even if it has a DealDamage behavior
    
    Useful if the action wants to decide when to CheckEvade 
    '''
    def __init__(self):
        super().__init__()
        
class AUGMENT_HERE(Flag):
    '''
    Mark where specifically an action can have augments added on the behavior list
    
    See AugmentDamage for default insertion logic
    '''
    def __init__(self):
        super().__init__()

        
class DMG_MULT(Flag):
    '''
    Mark to let the Action know to apply this damage multiplier 
    to all the subsequent AugmentDamage and DealDamage behaviors
    
    Can stack with other DMG_MULTs
    '''
    def __init__(self, mult:float):
        super().__init__()
        self.mult = mult
        
        


''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Battle Action ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
class BattleAction():
    def __init__(self, name:str, ap_cost:int, behaviors:list[Behavior],
                 valid_targets:list[TargetTypes] = [], 
                 ap_flexible:bool = False):
        self.name = name
        self.ap = ap_cost
        self.valid_targs = valid_targets
        # ap_flexible means for every ap_cost passed into the cast, its effects will occur
        # what each ap does is up for the FlexibleBehaviors to decide
        self.flexible = ap_flexible
        self.behaviors = behaviors
        
        self.evadable = False
        self.unevadable = False
        self.for_self = False
        
        # check that AugmentDamage(s) come before DealDamage (excluding Flags & Conditions) 
        # also while we're checking, if there is a DealDamage then this action is evadable
        # unless it is unevadable through behavior flag      
        auging = False
        for behavior in self.behaviors:
            # check that non Flag, Condition behaviors are setting this action for self
            if not isinstance(behavior, Flag) and not isinstance(behavior, Condition):
                if behavior.for_self:
                    self.for_self = True
            
            if isinstance(behavior, AugmentDamage):
                auging = True
            elif isinstance(behavior, UNEVADABLE):
                self.unevadable = True
            elif isinstance(behavior, DealDamage):
                auging = False
                self.evadable = not self.unevadable
            # can hold onto augs when going thru flags and conditions?
            elif auging and not (isinstance(behavior, Condition) or isinstance(behavior, Flag)):
                break
            
        if self.evadable:
            self.behaviors.insert(0, CheckEvade())
            
        if auging:
            raise Exception(
                ("AugmentDamage(s) must come before DealDamage and"
                + " there must be a DealDamage after AugmentDamage(s)")
                )
        
        # temporary modification of an action's behavior
        # Example: an electric glove may add a 0.1 of int DealDamage behavior to an action    
        self.behaviors_modified = copy.deepcopy(self.behaviors)
        
        self.action_type = self.get_action_type()
    
    def __repr__(self):
        return f"{self.name}, {self.ap} cost, {self.behaviors})"
    
    def __str__(self):
        flexible_suffix = "(Flexible)" if self.flexible else ""
        return f'{self.name} = {self.ap} AP {flexible_suffix}'
    
                
    def reset_behaviors(self):
            self.behaviors_modified = copy.deepcopy(self.behaviors)
    
    # TODO: account for non damage dealing behaviors
    def get_action_type(self):
        for behavior in self.behaviors_modified:
            if isinstance(behavior, DealDamage):
                if behavior.damage.is_heal:
                    return "heal"
                return "dmg"
        
        #TODO: what is default    
        #return "dmg"
        
    def cast(self, user:BattlePeep, target:BattlePeep, ap_spent:int):
        '''
        Calls of behaviors of the action utilizing passed in info
        
        @param user: user of the action
        @param target: target of the action
        @param ap_spent: amount of AP spent to cast this move. Only useful if this action is flexible
            as it dictates how many 'uses' of this action's behavior's
        '''
        
        if self.flexible and ap_spent % self.ap != 0:
            raise Exception("This action's cost must be a factor of ap_spent")
        
        auged_dmg = 0
        dmg_mult = 1
        cur_cond = True # if conditions are met
        sorting_out_condition = False # if last behavior analyzed was a condition
        
        # TODO: if ap flexible, cast for as many times as Ap used
        for behavior in self.behaviors_modified:
 
            # check if conditions are met    
            if isinstance(behavior, Condition):
                behavior.cur_cond = cur_cond
                if sorting_out_condition:
                    # if last behavior analyzed was a condition
                    # use AND or OR logic
                    cur_cond = (cur_cond and behavior.execute(user, target) 
                    if behavior.AND 
                    else cur_cond or behavior.execute(user, target)
                )
                else:
                    cur_cond = behavior.execute(user, target) 
                    sorting_out_condition = True
                continue
            
            elif not cur_cond: 
                sorting_out_condition = False
                continue
            ''' @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                Everything below is executed ONLY if conditions are met 
                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'''
            
            # check if the target would evade this attack
            if isinstance(behavior, CheckEvade):
                # stop cast if evaded
                if behavior.execute(user, target):
                    return
                else:
                    continue
            
            # not looking at a condition
            sorting_out_condition = False
            
            # Deal with Abort Behavior  
            if isinstance(behavior, ABORT):
                return
            
            # store damage mult to apply to subsequent damage behaviors
            if isinstance(behavior, DMG_MULT):
                dmg_mult *= behavior.mult
            
            # grab extra damage to add to final attack
            if isinstance(behavior, AugmentDamage):
                behavior.damage.mult = dmg_mult
                behavior.execute(user, target)
                auged_dmg += behavior.damage.amount
                continue
            
            # add aug dmg to DealDamage behavior   
            if auged_dmg != 0 and isinstance(behavior, DealDamage):
                behavior.damage.mult = dmg_mult
                behavior.damage.amount = auged_dmg
                auged_dmg = 0
            
            '''
            EXECUTE
            
            If flexible, pass in ap spent divided by ap cost (how many 'uses')
            '''
            if isinstance(behavior, FlexibleAPBehavior):
                behavior.execute(user, target, ap_spent//self.ap)   
            else: 
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
        
class TargetTypes(Enum):
    SELF = auto()
    ALLY = auto()
    ENEMY = auto()
    OBJECT = auto()
