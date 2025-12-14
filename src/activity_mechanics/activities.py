from enum import Enum, auto

from activity_mechanics.resources import Resource as ReS, ResourcesType as RT
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
                 stat_changes:list[StatChange],  
                 pips_req:float, 
                 tres_perc_cost:float,
                 cost:list[ReS] = [],
                 production:list[ReS] = [],
                 tags:list[Tag] = []):
        self.name = name
        self.tags = tags
        self.stat_changes = stat_changes
        self.pips_req = pips_req
        self.stress_percent_cost = tres_perc_cost
        self.rescource_cost = cost
        self.produced_resc = production
    
ACTIVITIES = [        
    Activity(
        "Workout", tags=[],
        stat_changes=[
            StatChange("str", 3, 1),
            StatChange("hun",-1, 0),
            StatChange("int", -1, -1),
        ],
        pips_req=2,
        tres_perc_cost=0.1),
    
    Activity(
        "Study", tags=[],
        stat_changes=[
            StatChange("int", 3, 2),
            StatChange("str",-1, 0),
        ],
        pips_req=3,
        tres_perc_cost=0.1),
    
    Activity(
        "Meditate", tags=[],
        stat_changes=[
            StatChange("tres", 1, 2),
        ],
        pips_req=2,
        tres_perc_cost=-0.2,
        ),
    
    Activity(
        "Patrol", tags=[],
        stat_changes=[
            StatChange("eva", 1, 2),
        ],
        pips_req=2,
        tres_perc_cost=-0.2,
        ),
    
    Activity(
        "Relieve Yourself", tags=[],
        stat_changes=[
            StatChange("tres", 1, 0),
            StatChange("cha",-1, -1),
        ],
        pips_req=1,
        tres_perc_cost=-0.1),
    
    # RESOURCE 
    
    Activity(
        "Clean", tags=[],
        stat_changes=[
            StatChange("dex", 1, 2),
            StatChange("rec", 1, 1),
            StatChange("def", -1, 1),
        ],
        pips_req=2,
        tres_perc_cost=0.3,
        production=[ReS(RT.CLEANLINESS, 10)]),
    
    Activity(
        "Farm", tags=[],
        stat_changes=[
            StatChange("rec", 1, 4),
        ],
        pips_req=4,
        tres_perc_cost=0.1,
        cost=[ReS(RT.SEEDS, 1)],
        production=[ReS(RT.INGREDIENTS, 2)],
        ),
    
    Activity(
        "Cook", tags=[],
        stat_changes=[
            StatChange("cre", 1, 2),
            StatChange("hun", 1, 1),
        ],
        pips_req=2,
        tres_perc_cost=0.2,
        cost=[ReS(RT.INGREDIENTS, 1)],
        production=[ReS(RT.FOOD, 2)],
        ),
    
    Activity(
        "Barricade", tags=[],
        stat_changes=[
            StatChange("def", 1, 4),
        ],
        pips_req=4,
        tres_perc_cost=0.3,
        cost=[ReS(RT.MATERIALS, 5)],
        production=[ReS(RT.DEFENSE, 5)],
        ),
    

]