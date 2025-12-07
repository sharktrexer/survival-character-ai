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
    '''
    Class that defines the details of an activity
    '''
    
    def __init__(self, name:str, 
                 tags:list[Tag], stat_changes:list[StatChange],  
                 pips_req:float, 
                 tres_perc_cost:float,
                 cost:list[Resource] = [],
                 production:list[Resource] = []):
        self.name = name
        self.tags = tags
        self.stat_changes = stat_changes
        self.pips_req = pips_req
        self.stress_percent_cost = tres_perc_cost
        self.rescource_cost = cost
        self.produced_resc = production
        
workout = Activity("Workout", tags=[],
                   stat_changes=[
                       StatChange("str", 3, 1),
                       StatChange("hun",-1, 0),
                   ],
                   pips_req=2,
                   tres_perc_cost=0.1)