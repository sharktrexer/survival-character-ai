from enum import Enum, auto
from copy import deepcopy

class ResourcesType(Enum):
    SEEDS = auto()
    INGREDIENTS = auto()
    FOOD = auto()
    
    MATERIALS = auto()
    DEFENSE = auto()
    
class Resource():
    def __init__(self, r_type:ResourcesType, amount:int):
        self.type = r_type
        self.amount = amount
        
    def __eq__(self, other):
        return isinstance(other, Resource) and self.type == other.type
 
 
RESOURCE_LIST = [Resource(r_type, 0) for r_type in ResourcesType]
    
class ResourceManager:
    '''
    Manages the resources owned by the lodge.
    '''
    def __init__(self, resources:list[Resource] = []):
        if resources != []:
            self.resources = {r.type: r for r in resources}
        else:
            self.resources = {r.type: r for r in RESOURCE_LIST}
        
    def does_this_cover_cost(self, cost:list[Resource]) -> bool:
        
        """
        Determines whether the owned resources are sufficient to cover the costs.
        """
        
        for r in cost:
            if self.resources[r.type].amount < r.amount:
                return False
        return True
    
    def exchange(self, cost:list[Resource]) -> bool:
        """
        Exchanges resources according to the inputted cost.
        
        Returns True if the exchange was successful
        """
        
        temp_resources = deepcopy(self.resources)
        
        for r in cost:
            if self.resources[r.type].amount < r.amount:
                return False
            temp_resources[r.type].amount -= r.amount
            
        self.resources = deepcopy(temp_resources)
        return True
            