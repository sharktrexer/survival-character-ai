from copy import deepcopy
import math
import random

from activity_mechanics.activities import Activity, ACTIVITIES, Objective
from activity_mechanics.activity_manager import ActivityManager
from activity_mechanics.cooking import Meal, MEALS
from activity_mechanics.progress import ActivityProgress
from activity_mechanics.resources import Resource, ResourceManager, ResourcesType
from activity_mechanics.time_management import TimeKeeper
from activity_mechanics.farming import PLANTS, Plant
from activity_mechanics.house_keeping import BARRICADES, Barricade, Clean

from battle.battle_peep import BattlePeep
from utils.helpers import Calcs
from peep_data.data_reader import PEEPS

class Room:
    def __init__(self, name:str, exits:list[Room]=[], cleanliness=100):
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
        
        self.activity_man = ActivityManager()
        self.peep_time_awake: dict[str,int] = {p.name:0 for p in PEEPS}
        self.rooms = {r.name:r for r in deepcopy(ROOMS)}
        self.made_stuff: list[Objective] = []
        
        self.cleanliness = 0
        self.update_cleanliness()
    
    def reset(self):
        self.time_keeper = TimeKeeper()
        self.resourcer = ResourceManager()
        self.rooms = {r.name:r for r in deepcopy(ROOMS)}
        self.update_cleanliness()
    
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
        return peep.points_of('tres') - activity.get_stress_cost() >= 0
    
    def exchange_resources(self, cost:list[Resource]):
        self.resourcer.exchange(cost)
    
    def obtain_resources(self, gain:list[Resource]):
        self.resourcer.obtain(gain)
    
    def tick_lodge(self):
        self.time_keeper.tick()
        
        # track how long peeps are awake
        for peep in self.peep_time_awake.keys():
            # tick up ones who are not sleeping
            self.peep_time_awake[peep] += 1
            
        '''
        Tick everyone's hunger down
        '''
        

                    
        
    def finish_activity(self, peep:BattlePeep, activity_prog:ActivityProgress):
        
        group_size = activity_prog.get_group_size()
        
        def cgb(val:int):
            '''
            Calculate Group Bonus
            
            Gives the activity's values a bonus based on group size
            '''
            courtesy_bonus = 1 if group_size > 1 and val != 0 else 0
            percent_chng   = (abs(val) * 0.1 * (group_size - 1)) + courtesy_bonus
            
            # increase positive changes or reduce negative changes 
            result = round(val + percent_chng )
            
            return result
        
        activity = activity_prog.activity
        
        # stat effects
        for chng in activity.stat_changes:
            peep.stats.grow_stat(chng.name, cgb(chng.val_amount), cgb(chng.apt_xp_amount))
            
        # all resource effects
        for cost in activity.gauge_costs:
            peep.stats.resource_change(cost.name, cgb(cost.val_amount))
            
        # deal with objective
        if activity.objective != None:
            self.made_stuff.append(activity.objective)
        
        # dirty the room from use
        if activity.name != 'Clean':   
            self.rooms[activity.location].clean(-5)
        
        
    def cook(self, peep:BattlePeep, meal:Meal):
        dirtiness = -10
        self.rooms['Kitchen'].clean(dirtiness)
    
    def eat(self, peep:BattlePeep, meal:Meal):
        dirtiness = -5
        self.rooms['Kitchen'].clean(dirtiness)
    
    def sleep(self, peep:BattlePeep):
        pass
    
    def clean_from_objective(self, clean_obj:Clean):
        self.rooms[clean_obj.room].clean(clean_obj.clean_yield)
        self.update_cleanliness()
    
    def update_clean_act(self, peep:BattlePeep, room:Room, act:Activity):
        dex_apt = peep.stats.get_stat_apt('dex')
        
        # change amount based on aptitude
        clean_amnt = 5
        if dex_apt > 1:
            clean_amnt *= dex_apt 
        elif dex_apt < 0:
            clean_amnt += dex_apt * 2
            
        act.objective = Clean(f'Cleaning {room.name}', clean_amnt, room.name)
        act.location = room.name
    
    def game(self, peep:BattlePeep, game):
        pass

    def end_day(self):
        self.creep_grime()
    

        