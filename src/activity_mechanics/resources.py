from enum import Enum, auto
from copy import deepcopy
from utils.helpers import Calcs

class ResourcesType(Enum):
    SEEDS = auto()
    INGREDIENTS = auto()
    FOOD = auto()
    
    MATERIALS = auto()
    DEFENSE = auto()
    
    CLEANLINESS = auto()
    
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
        if len(resources) != len(ResourcesType):
            raise Exception((f"Incorrect number of resources provided:" 
                             f" entered {len(resources)} vs"
                             f" {len(ResourcesType)} types of resources!"))
        
        if resources != []:
            self.resources = {r.type: r for r in resources}
        else:
            self.resources = {r.type: r for r in EMPTY_RESOURCE_LIST}
            self.resources[ResourcesType.CLEANLINESS].amount = 100
            
        self.cap_grime()
    
    def obtain(self, gain:list[Resource]):
        for r in gain:
            self.resources[r.type].amount += r.amount
            
        self.cap_grime()
    
    def cap_grime(self):
        '''
        Grime works as a gauge, from 0-100 (clean to dirty)
        Anytime the grime resource could be changed, clamp it
        '''
        self.resources[ResourcesType.CLEANLINESS].amount = (
            Calcs.clamp_int(self.resources[ResourcesType.CLEANLINESS].amount, min_v=0, max_v=100)
            )
         
            
    def exchange(self, cost:list[Resource], do_update:bool = True) -> list[Resource]:
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
                return None
            temp_resources[r.type].amount -= r.amount
            temp_resources[r.type].amount = max(0, temp_resources[r.type].amount)
        
        if do_update:    
            self.update_resources(temp_resources)
        return temp_resources
    
    def update_resources(self, resources:list[Resource]):
        self.resources = deepcopy(resources)
        self.cap_grime()
            