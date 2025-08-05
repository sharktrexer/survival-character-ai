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
    def __init__(self, resources:dict[ResourcesTypes, Resource]):
        self.resources = resources
        pass