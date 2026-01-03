from copy import deepcopy
import math
import random
from activity_mechanics.activities import Activity
from activity_mechanics.cooking import Meal, MEALS
from activity_mechanics.resources import Resource, ResourceManager, ResourcesType
from activity_mechanics.time_management import TimeKeeper
from peep_data.data_reader import PEEPS

from activity_mechanics.farming import PLANTS, Plant
from activity_mechanics.barricading import BARRICADES, Barricade

from battle.battle_peep import BattlePeep
from utils.helpers import Calcs

class Room:
    def __init__(self, name, exits:list[Room]=[], cleanliness=100):
        self.name = name
        self.cleanliness = cleanliness
        
    def clean(self, amount):
        self.cleanliness += amount
        self.cleanliness = Calcs.clamp_100(self.cleanliness)
        

ROOMS = [
    Room('Kitchen'),
    Room('Locker Room'),
    Room('Foyer'),
    Room('Living Room'),
    Room('Gym'),
]

class Lodge:
    '''
    Info stored representing the state of the lodge
    
    Track the location of each peep, current activity they are doing
    
    '''
    def __init__(self, name, resourcer:ResourceManager):
        self.name = name
        self.resourcer = resourcer
        self.time_keeper = TimeKeeper()
        self.rooms = {r.name:r for r in deepcopy(ROOMS)}
        self.cleanliness = 0
        self.update_cleanliness()
        self.peep_time_awake = {p.name:0 for p in PEEPS}
    
    def reset(self):
        self.time_keeper = TimeKeeper()
        self.resourcer = ResourceManager()
        self.rooms = {r.name:r for r in deepcopy(ROOMS)}
        self.update_cleanliness()
        self.peep_time_awake = {p.name:0 for p in PEEPS}
    
    def creep_grime(self):
        '''
        Randomly make a room dirty by 5 every day
        '''
        rand_room_key = random.choice(list(self.rooms.keys()))
        self.rooms[rand_room_key].clean(-5)
    
    def update_cleanliness(self):
        self.cleanliness = sum([r.cleanliness for r in list(self.rooms.values())])    
    
    def check_stress(self, peep:BattlePeep, activity:Activity):
        '''
        if the peep is calm enough to do the activity
        '''
        return peep.points_of('tres') - activity.stress_cost >= 0
    
    def exchange_resources(self, cost:list[Resource]):
        self.resourcer.exchange(cost)
    
    def obtain_resources(self, gain:list[Resource]):
        self.resourcer.obtain(gain)
        
    def do_activity(self, peep:BattlePeep, activity:Activity):
        
        # time goes by
        #TODO: what happens if ambushed!?
        self.time_keeper.tick_by_pip(activity.time_pip_cost)
        
        # stat effects
        for chng in activity.stat_changes:
            peep.stats.grow_stat(chng.name, chng.val_amount, chng.apt_xp_amount)
            
        # all resource effects
        for cost in activity.gauge_costs:
            peep.stats.resource_change(cost.name, cost.val_amount)
        
        #TODO: hunger resource affect
        
    def cook(self, peep:BattlePeep, meal:Meal):
        dirtiness = -10
        self.rooms['Kitchen'].clean(dirtiness)
    
    def eat(self, peep:BattlePeep, meal:Meal):
        dirtiness = -5
        self.rooms['Kitchen'].clean(dirtiness)
    
    def sleep(self, peep:BattlePeep):
        pass
    
    def clean(self, peep:BattlePeep, room:Room):
        self.update_cleanliness()
        pass
    
    def game(self, peep:BattlePeep, game):
        pass

    def end_day(self):
        self.creep_grime()
    
        