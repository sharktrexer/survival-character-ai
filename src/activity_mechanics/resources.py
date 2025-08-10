from enum import Enum, auto


class ResourcesTypes(Enum):
    SEEDS = auto()
    INGREDIENTS = auto()
    FOOD = auto()
    
    MATERIALS = auto()
    DEFENSE = auto()
    
class Resource():
    def __init__(self, r_type:ResourcesTypes, amount:int):
        self.type = r_type
        self.amount = amount
        
    def __eq__(self, other):
        return isinstance(other, Resource) and self.type == other.type
 
 
RESOURCE_LIST = [Resource(r_type, 0) for r_type in ResourcesTypes]
    
    
''' To replace resource exchanger'''
class ResourceManager:
    def __init__(self):
        self.resources = RESOURCE_LIST
        
    def does_this_cover_cost(self, cost:list[Resource]):
        
        """
        Determines whether the owned resources are sufficient to cover the costs.

        Parameters:
            cost (list[Resource]): A list of resources required to be consumed. 
                Every type of resource is assumed to be represented in this list.

        Returns:
            bool: if all resources in the cost list are covered by the owned resources
        """

        for i, r_cost in enumerate(cost):
            if self.resources[i].amount < r_cost.amount:
                return False
        return True
    
    def exchange(self, cost:list[Resource]):
        """
        Exchanges resources according to the inputted cost.

        Parameters:
            owned_resources (list[Resource]): A list of resources currently owned. 
                Every type of resource is assumed to be represented in this list.

        Returns:
            bool: if the exchange is successful.
        """
        temp_resources = self.resources[:]
        
        for i, r_cost in enumerate(cost):
            if self.resources[i].amount - r_cost.amount < 0:
                return False
            temp_resources[i].amount -= r_cost.amount
            
        self.resources = temp_resources[:]
        return True
            