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
        
    def cast(self, user:BattlePeep, target:BattlePeep):
        
        auged_dmg = 0
        
        for behavior in self.behaviors:
            
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
            
    def get_damage_per_stat(self):
        
        stat_2_dmg_dict = {}
        
        # get ratios of stats used for damage
        # TODO: handle decreases in healing (thru dmg augs) and decreases in damage (heal augs)
        for behavior in self.behaviors:
            
            if isinstance(behavior, AugmentDamage) or isinstance(behavior, DealDamage):
                
                if behavior.damage.empowering_stat not in stat_2_dmg_dict:
                    stat_2_dmg_dict[behavior.damage.empowering_stat] = 0 # initialize key
                    
                stat_2_dmg_dict[behavior.damage.empowering_stat] += behavior.damage.ratio
                
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