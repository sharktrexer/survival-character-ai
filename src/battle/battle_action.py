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
    def __init__(self, name:str, behaviors:list[Behavior]):
        self.name = name
        self.behaviors = behaviors
        
        # check that AugmentDamage(s) come before DealDamage        
        auging = False
        for behavior in self.behaviors:
            if isinstance(behavior, AugmentDamage):
                auging = True
            elif isinstance(behavior, DealDamage):
                auging = False
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
        
        for behavior in self.behaviors_modified:
            
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



