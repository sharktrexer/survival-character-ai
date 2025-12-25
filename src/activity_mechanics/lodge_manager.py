from copy import deepcopy
import math
import random
from activity_mechanics.activities import Activity
from activity_mechanics.cooking import Meal
from activity_mechanics.resources import Resource, ResourceManager, ResourcesType
from activity_mechanics.time_management import TimeKeeper
from peep_data.data_reader import PEEPS

from cooking import MEALS, Meal
from farming import PLANTS, Plant
from barricading import BARRICADES, Barricade

from battle.battle_peep import BattlePeep
from utils.helpers import Calcs

class Room:
    def __init__(self, name, cleanliness=100):
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
    '''
    def __init__(self, name, resourcer:ResourceManager):
        self.name = name
        self.resourcer = resourcer
        self.time_keeper = TimeKeeper()
        self.rooms = {r.name:r for r in deepcopy(ROOMS)}
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
        self.cleanliness = sum([r.cleanliness for r in self.rooms])    
        
    def do_activity(self, peep:BattlePeep, activity:Activity):
        
        #TODO: can the peep take the hunger hit?
        
        # can the peep take the stress hit!?   
        tres_effct = activity.stress_cost * peep.value_of('tres')
        is_calm_enough = peep.points_of('tres') - tres_effct >= 0
        if not is_calm_enough:
            return False
        
        # resource exchange, if possible
        lodge_resources = self.resourcer.exchange(activity.rescource_cost, do_update=False)
        if lodge_resources is None:
            return False
        else:
            self.resourcer.update_resources(lodge_resources)
        
        # dirty the room
        if activity.location in list(self.rooms.keys()):
            # every pip of time is equivelent to 0.5 points of dirtiness, ceiled up
            dirtiness = math.ceil(0.5 * activity.time_cost)
            self.rooms[activity.location].clean(dirtiness)
        
        # time goes by
        #TODO: what happens if ambushed!?
        self.time_keeper.tick_by_pip(activity.time_cost)
        
        # stat effects
        for chng in activity.stat_changes:
            peep.stats.grow_stat(chng.name, chng.val_amount, chng.apt_xp_amount)
            
        # stress resource effect
        peep.stats.resource_change("stress", tres_effct)
        
        # get resources produced, if possible
        #TODO: what if obtained vars is based on what happens in activity?
        self.resourcer.obtain(activity.produced_resc)
        
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
    
    def calc_hrs_req_to_sleep(self, peep:BattlePeep):
        '''
        Time Spent Asleep:
        With 0 Energy Aptitude or Higher: 
            peeps need 8 hours of sleep.
        Per point of Energy Apt below 0: 
            peeps need +1 more hrs of sleep (12 max)
        '''
        if peep.apt_of('ap)') >= 0:
            return 8
        else:
            return 8 - self.cur_stats["energy"].apt

    def end_day(self):
        self.creep_grime()
    
        