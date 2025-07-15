from enum import Enum, auto

class Tag(Enum):
    WORK = auto()
    LEISURE = auto()   
    
    RESOURCE_PRODUCING = auto()
    RESOURCE_USING = auto()
    RESOURCE_PROCESSING = auto()
    
    INDOORS = auto()
    OUTDOORS = auto()
    
class ResourcesTypes(Enum):
    FOOD = auto()
    INGREDIENTS = auto()
    MATERIALS = auto()
    
class Resource():
    def __init__(self, r_type:ResourcesTypes, amount:int):
        self.type = r_type
        self.amount = amount
        
    def __eq__(self, other):
        return isinstance(other, Resource) and self.type == other.type

RESOURCE_LIST = [Resource(r_type, 0) for r_type in ResourcesTypes]

class ResourceExchanger():
    def __init__(self, costs:list[Resource], produces:list[Resource]):
        self.costs = costs
        self.produces = produces
        
    def does_this_cover_cost(self, owned_resources:list[Resource]):
        for cost in self.costs:
            for owned in owned_resources:
                if cost == owned: 
                    if cost.amount > owned.amount:
                        return False
        return True

class StatChange():
    def __init__(self, stat_name:str, val_amount:int, apt_amount:int):
        self.name = stat_name
        self.val_amount = val_amount
        self.apt_amount = apt_amount

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
    