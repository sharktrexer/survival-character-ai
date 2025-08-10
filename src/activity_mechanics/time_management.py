'''
For keeping track of time in minutes, including per move in combat, and per actiivity done
'''
from enum import Enum, auto

class Season(Enum):
    WINTER = auto()
    SPRING = auto()
    SUMMER = auto()
    FALL = auto()

class TimeOfDay(Enum):
    DAY = auto()
    NIGHT = auto()
    
MINS_PER_TURN = 15
HRS_IN_DAY = 24

def get_day_n_night_hrs_by_season(seas:Season):
    # day in hrs, night in hrs
    if seas == Season.WINTER:
        return 8, 16 # 8 hr day
    elif seas == Season.SPRING or seas == Season.FALL:
        return 12, 12 # 12 hr day
    elif seas == Season.SUMMER:
        return 16, 8 # 16 hr day

class TimeKeeper:
    def __init__(self, season:Season):
        self.season = season
        self.day = 0
        self.cur_hr = 0
        self.cur_min = 0
        self.time_of_day = TimeOfDay.DAY
        
    def calc_time_of_day(self):
        day_hrs, night_hrs = get_day_n_night_hrs_by_season(self.season)
        
        if ((self.cur_hr >= 0 and self.cur_hr < night_hrs / 2)
            or self.cur_hr >= night_hrs / 2 + day_hrs
            ):
            self.time_of_day = TimeOfDay.NIGHT
        else:
            self.time_of_day = TimeOfDay.DAY
    
    def tick(self):
        self.cur_min += 1
        self.cur_hr = self.cur_min % 60
        
        self.change_time_of_day()
        
    def tick_turn(self):
        self.cur_min += MINS_PER_TURN
        self.cur_hr = self.cur_min % 60
        
        self.change_time_of_day()
            
    def change_time_of_day(self):
        
        # check for a new day
        if self.cur_hr == HRS_IN_DAY:
            self.cur_min -= HRS_IN_DAY * 60
            self.cur_hr = 0
            self.day += 1
            
        self.calc_time_of_day()
        
    
