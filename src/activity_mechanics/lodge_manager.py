from copy import deepcopy
import math
import random

from activity_mechanics.activities import Activity, ACTIVITIES, ActResult, SimpleResult
from activity_mechanics.activity_manager import ActivityManager
from activity_mechanics.cooking import Meal, MEALS
from activity_mechanics.progress import ActivityProgress
from activity_mechanics.resources import Resource, ResourceManager, ResourcesType
from activity_mechanics.time_management import TimeKeeper
from activity_mechanics.farming import PLANTS, Plant

from battle.battle_peep import BattlePeep
from battle.stats import get_mult_of_aptitude
from utils.helpers import Calcs
from peep_data.data_reader import PEEPS

class Room:
    def __init__(self, name:str, exits:list[Room]=[], cleanliness=100):
        self.name = name
        self.cleanliness = cleanliness
        self.defense = 0
        self.max_defense = 50
        
    def clean(self, amount):
        self.cleanliness += amount
        self.cleanliness = Calcs.clamp_100(self.cleanliness)
        
    def barricade(self, amount):
        self.defense += amount
        self.defense = Calcs.clamp_int(self.defense, min_v=0, max_v=self.max_defense)
        

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
        self.made_stuff: list[ActResult] = []
        
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
        # don't store simple results
        if activity.objective != None and not isinstance(activity.objective, SimpleResult):
            self.made_stuff.append(activity.objective)
        
        # hurt peep if room cleanliness is == 0
        # +50% stress if cleanliness is <= 25
        
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
    
    def apply_simple_act_rslt(self, act:Activity):
        '''
        Apply the specific changes made to the lodge from the simple result
        of the activity.
        
        Returns a tuple of the old and new value changed
        '''
        room = self.rooms[act.location]
        
        past_val:int = 0
        new_val:int = 0
        match(act.name):
            case 'Clean':
                past_val = room.cleanliness
                room.clean(act.objective.change)
                self.update_cleanliness()
                new_val = room.cleanliness
                
            case 'Barricade':
                past_val = room.defense
                room.barricade(act.objective.change)
                new_val = room.defense
                
            case _:
                raise Exception(f'Unknown activity to apply simple result from: {act.name}')
            
        return (past_val, new_val)
    
    def update_simple_result(self, peep:BattlePeep, room:Room, act:Activity):        
        stat = ''
        match(act.name):
            case 'Clean':
                stat = 'dex'
            case 'Barricade':
                stat = 'def'
                self.resourcer.exchange([Resource(ResourcesType.MATERIALS, 10)])
            case _:
                raise Exception(f'Unknown Activity to updare simple result of: {act.name}')
            
        # change amount based on aptitude
        amnt = round(10 * get_mult_of_aptitude(peep.stats.get_stat_apt(stat)))

        act.location = room.name
        act.objective = SimpleResult(f'{act.name}ing {room.name}', amnt, room.name)

    
    def game(self, peep:BattlePeep, game):
        pass

    def end_day(self):
        self.creep_grime()
    

        