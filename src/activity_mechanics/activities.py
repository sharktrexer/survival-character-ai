from enum import Enum, auto

from battle.battle_peep import BattlePeep
from activity_mechanics.resources import Resource, ResourceManager

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
    
    


class ResourceExchanger():
    def __init__(self, costs:list[Resource], produces:list[Resource]):
        self.costs = costs
        self.produces = produces
        
    def does_this_cover_cost(self, owned_resources:list[Resource]):
        
        """
        Determines whether the owned resources are sufficient to cover the costs.

        Parameters:
            owned_resources (list[Resource]): A list of resources currently owned. 
                Every type of resource is assumed to be represented in this list.

        Returns:
            bool: True if all resources in the costs list are covered by the owned resources,
                  False otherwise.
        """

        for cost in self.costs:
            for owned in owned_resources:
                if cost != owned: 
                    continue
                if cost.amount > owned.amount:
                    return False
        return True
    
    def exchange(self, owned_resources:list[Resource]):
        """
        Exchanges resources according to the costs and produces defined in this
        ResourceExchanger.

        Parameters:
            owned_resources (list[Resource]): A list of resources currently owned. 
                Every type of resource is assumed to be represented in this list.

        Returns:
            bool: True if the exchange is successful, False otherwise.
        """

        enough_owned = self.does_this_cover_cost(owned_resources)
        
        if not enough_owned:
            return False
        
        # consume resources
        for cost in self.costs:
            for owned in owned_resources:
                if cost != owned:
                    continue 
                owned.amount -= cost.amount
                
        # if no resources to produce
        if self.produces is None:
            return True
        
        # produce resources
        for produce in self.produces:
            for owned in owned_resources:
                if produce != owned:
                    continue
                owned.amount += produce.amount
        return True

class StatChange():
    def __init__(self, stat_name:str, val_amount:int, apt_xp_amount:int):
        self.name = stat_name
        self.val_amount = val_amount
        self.apt_xp_amount = apt_xp_amount

class Activity():
    
    def __init__(self, name:str, 
                 tags:list[Tag], stat_changes:list[StatChange],  
                 hours_required:float, 
                 stress_effect:int,
                 exchanger:ResourceExchanger):
        self.name = name
        self.tags = tags
        self.stat_changes = stat_changes
        self.hours_required = hours_required
        self.stress_effect = stress_effect
        self.exchanger = exchanger
    
    def affect_peep(self, peep:BattlePeep):
        
        # stat effects
        for stat_change in self.stat_changes:
            #TODO: multiply by status effects on peep
            peep.stats.change_apt_xp(stat_change.name, stat_change.apt_xp_amount)
            peep.stats.change_stat_base_val(stat_change.name, stat_change.val_amount)
            
        # stress resource effect
        peep.stats.resource_change("stress", self.stress_effect)
        
        # hunger resource effect
        #TODO: mult of hunger resource consumption due to activity
            
    def do(self, peep:BattlePeep):
        
        do = self.exchanger.exchange(peep.resources)
        if do:
            #TODO: affect stress, 
            self.affect_peep(peep)
        
        return do