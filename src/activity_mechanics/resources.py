from enum import Enum, auto
from copy import deepcopy
from utils.helpers import Calcs

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
        if len(resources) != 0 and len(resources) != len(ResourcesType):
            raise Exception((f"Incorrect number of resources provided:" 
                             f" entered {len(resources)} vs"
                             f" {len(ResourcesType)} types of resources!"))
        
        if resources != []:
            self.resources = {r.type: r for r in resources}
        else:
            self.resources = {r.type: r for r in EMPTY_RESOURCE_LIST}
            
    
    def obtain(self, gain:list[Resource]):
        for r in gain:
            self.resources[r.type].amount += r.amount
            
        self.cap_grime()
         
    
    def can_cover_the_cost(self, cost:list[Resource]): 
        for r in cost:
            if self.resources[r.type].amount < r.amount:
                return False
            
        return True
            
    def exchange(self, cost:list[Resource]) -> list[Resource]:
        """
        Exchanges resources according to the inputted cost.
        
        Includes failsafe to abort if a resource cost is not met
        """
        if cost == []:
            return
        
        temp_resources = deepcopy(self.resources)
        
        for r in cost:
            if self.resources[r.type].amount < r.amount:
                raise Exception(f"Not enough resources to cover the cost! {self.resources[r.type].amount} < {r.amount}")
            temp_resources[r.type].amount -= r.amount
            temp_resources[r.type].amount = max(0, temp_resources[r.type].amount)
        
        self.update_resources(temp_resources)

    
    def update_resources(self, resources:list[Resource]):
        self.resources = deepcopy(resources)
        self.cap_grime()
            