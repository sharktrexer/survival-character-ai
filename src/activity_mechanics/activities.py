from enum import Enum, auto

from battle.battle_peep import BattlePeep
from activity_mechanics.resources import Resource, ResourceManager
from battle.stats import StatChange

class Tag(Enum):
    WORK = auto()
    LEISURE = auto()   
    
    RESOURCE_PRODUCING = auto()
    RESOURCE_USING = auto()
    RESOURCE_PROCESSING = auto()
    
    INDOORS = auto()
    OUTDOORS = auto()
    
    FLOOR1 = auto()
    FLOOR2 = auto()
    
    PHYSICAL = auto()
    EMOTIONAL = auto()
    MIXED = auto()

class Activity():
    
    def __init__(self, name:str, 
                 tags:list[Tag], stat_changes:list[StatChange],  
                 mins_req:float, 
                 stress_effect:int,
                 cost:list[Resource],
                 production:list[Resource]):
        self.name = name
        self.tags = tags
        self.stat_changes = stat_changes
        self.mins_required = mins_req
        self.stress_effect = stress_effect
        self.cost = cost
        self.production = production
    
    def affect_peep(self, peep:BattlePeep, mins_passed:int):
        
        time_mult = self.mins_required / mins_passed
        
        # stat effects
        for stat_change in self.stat_changes:
            
            # get value proportional to time passed on activity
            xp_change = stat_change.apt_xp_amount * time_mult
            val_change = stat_change.val_amount * time_mult
            #TODO: multiply by status effects on peep
            
            if stat_change.apt_xp_amount != 0:
                peep.stats.change_apt_xp(stat_change.name, stat_change.apt_xp_amount)
            if stat_change.val_amount != 0:
                peep.stats.change_stat_base_val(stat_change.name, stat_change.val_amount)
            # prevent func calls if a change is 0
            
        # stress resource effect
        peep.stats.resource_change("stress", self.stress_effect)
        
        # give peep an item or items
        if time_mult == 1:
            self.give_reward()
            
    def do(self, peep:BattlePeep):
        
        do = self.exchanger.exchange(peep.resources)
        if do:
            #TODO: affect stress, 
            self.affect_peep(peep)
        
        return do
    
    def give_reward():
        pass