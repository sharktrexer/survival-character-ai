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
    
    An activity must take up at least one hour, and can use multiplies of 15 minutes (one pip)
    '''
    
    def __init__(self, name:str, 
                 stat_changes:list[StatChange],  
                 time_pip_cost:int, 
                 tres_cost:int, # how much stress used
                 location:str,
                 cost:list[ReS] = [],
                 production:list[ReS] = [],
                 tags:list[Tag] = []):
        self.name = name
        self.tags = tags
        self.stat_changes = stat_changes
        self.time_pip_cost = time_pip_cost
        self.pip_progress = 0
        self.stress_cost = tres_cost
        self.location = location
        self.rescource_cost = cost
        self.produced_resc = production
        
        
        self.active_peeps: dict[str,int] = {}
        '''
        Dictionary of peep names who are doing the activity and their pip progress
        '''
        
    def __str__(self):
        return (f"{self.name} {self.stat_chnges_as_str()}"
            + f" [Pips: {self.time_pip_cost}] | [Stress: {self.stress_cost}]")
    
    def stat_chnges_as_str(self):
        str = []
        
        for s in self.stat_changes:
            val_sign = '+' if s.val_amount > 0 else ''
            apt_sign = '+' if s.apt_xp_amount > 0 else ''
            str.append(f"| {s.name} ({val_sign}{s.val_amount}val {apt_sign}{s.val_amount}xp) ")
        return "".join(str)
    
ACTIVITIES = [        
    Activity(
        "Workout", tags=[],
        stat_changes=[
            StatChange("str", 3, 1),
            StatChange("hun",-1, 0),
            StatChange("int", -1, -1),
        ],
        time_pip_cost=4,
        tres_cost=15,
        location='Gym'),
    
    Activity(
        "Study", tags=[],
        stat_changes=[
            StatChange("int", 3, 2),
            StatChange("str",-1, 0),
        ],
        time_pip_cost=5,
        tres_cost=15,
        location='Foyer'),
    
    Activity(
        "Meditate", tags=[],
        stat_changes=[
            StatChange("tres", 1, 2),
        ],
        time_pip_cost=6,
        tres_cost=-20,
        location='Outside'),
    
    Activity(
        "Patrol", tags=[],
        stat_changes=[
            StatChange("eva", 3, 2),
        ],
        time_pip_cost=5,
        tres_cost=20,
        location='Outside'
        ),
    
    Activity(
        "Relieve Yourself", tags=[],
        stat_changes=[
            StatChange("tres", 3, 0),
            StatChange("cha",-2, -2),
        ],
        time_pip_cost=4,
        tres_cost=-15,
        location='Locker Room'),
    
    Activity(
        "Game", tags=[],
        stat_changes=[
            StatChange("dex", 2, 3),
            StatChange("tres", 1, 0),
            StatChange("ap", -1, 0),
        ],
        time_pip_cost=4,
        tres_cost=-10,
        location='Living Room'),
    
    Activity(
        "Gaze Upon Your Visage", tags=[],
        stat_changes=[
            StatChange("cha", 2, 1),
            StatChange("tres", 1, 0),
            StatChange("rec", -1, -1),
        ],
        time_pip_cost=6,
        tres_cost=-5,
        location='Locker Room'),

    Activity(
        "Practice Your Mean Face", tags=[],
        stat_changes=[
            StatChange("itmd", 2, 1),
            StatChange("fear", 1, 0),
            StatChange("cha", -1, -1),
        ],
        time_pip_cost=4,
        tres_cost=-10,
        location='Locker Room'),

]