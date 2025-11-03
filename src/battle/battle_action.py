from .battle_peep import BattlePeep, Damage
from .damage import create_dmg
from .status_effects import StatusEffect
from .alteration import Alteration

class Behavior:
    '''
    Abstract class for behaviors
    '''
    def __init__(self, for_self:bool = False):
        self.for_self = for_self
    
    def execute(self, user:BattlePeep, target:BattlePeep):
        raise NotImplementedError("Method was not implemented despite inheriting from Behavior")
    
class DealDamage(Behavior):
    def __init__(self, damage:Damage, for_self:bool = False):
        super().__init__(for_self)
        self.damage = damage
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        self.damage.give_value(user.stats.get_stat_active(self.damage.empowering_stat))
        if self.for_self:
            user.affect_hp(self.damage)
            
        else:
            target.affect_hp(self.damage)
            #print(f' Dealing {self.damage.amount}')
        
class ApplyStatusEfct(Behavior):
    def __init__(self, stat_effect:StatusEffect, for_self:bool = False):
        super().__init__(for_self)
        self.stat_effect = stat_effect
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        if self.for_self:
            user.status_effects.append(self.stat_effect)
        else:
            self.stat_effect.apply(target, user)
        

class ApplyAlteration(Behavior):
    def __init__(self, alteration:Alteration, for_self:bool = False):
        super().__init__(for_self)
        self.alteration = alteration        
        
    def execute(self, user:BattlePeep, target:BattlePeep):
        target.recieve_alt(self.alteration)
        
class BattleAction():
    def __init__(self, name:str, behaviors:list[Behavior]):
        self.name = name
        self.behaviors = behaviors
        
    def cast(self, user:BattlePeep, target:BattlePeep):
        for behavior in self.behaviors:
            behavior.execute(user, target)

basic_heal = BattleAction("Heal",[
    DealDamage(create_dmg(0.8, Damage.DamageType.Healing))
])

basic_dmg = BattleAction("Attack",[
    DealDamage(create_dmg(0.6, Damage.DamageType.Physical))
])
            
rat_chz = BattleAction("Cheese Plate",[
    DealDamage(create_dmg(0.3, Damage.DamageType.Healing), for_self=True),
    DealDamage(create_dmg(0.8, Damage.DamageType.Healing))
])