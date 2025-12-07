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
 
 
EMPTY_RESOURCE_LIST = [Resource(r_type, 0) for r_type in ResourcesType]
    
class ResourceManager:
    '''
    Manages the resources owned by the lodge.
    '''
    def __init__(self, resources:list[Resource] = []):
        '''
        Constructor
        
        Creates a resource list with the given resources
        If none is provided, default resource with each starting at 0 is created
        '''
        if resources != []:
            self.resources = {r.type.name: r for r in resources}
        else:
            self.resources = {r.type.name: r for r in EMPTY_RESOURCE_LIST}
    
    def obtain(self, gain:list[Resource]):
        for r in gain:
            self.resources[r.type.name].amount += r.amount
            
    def exchange(self, cost:list[Resource]) -> bool:
        """
        Exchanges resources according to the inputted cost.
        
        Returns True if the exchange was successful
        
        Otherwise, returns false and maintains current resources
        """
        if cost == []:
            return True
        
        temp_resources = deepcopy(self.resources)
        
        for r in cost:
            if self.resources[r.type].amount < r.amount:
                return False
            temp_resources[r.type].amount -= r.amount
            
        self.resources = deepcopy(temp_resources)
        
        return True
            