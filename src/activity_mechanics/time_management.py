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
    
MINS_PER_TURN = 10
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
    def __init__(self):
        self.season = Season.WINTER
        self.days_passed = 0
        self.cur_hr = 0
        self.cur_min = 0
        self.time_of_day = TimeOfDay.DAY
        self.day_hrs, self.night_hrs = get_day_n_night_hrs_by_season(self.season)
    
    def update_season(self):
        
        # every 5 days change season 
        #    5   -   5   -   5   - 5
        # Winter, Spring, Summer, Fall
        #          4 seasons
        #         |_________\
        #     25 Days in the 'Year'
        #     4 years in 100 days
        season_input = self.days_passed // 5 % 4
            
        match(season_input):
            case 0:
                self.season = Season.WINTER
            case 1:
                self.season = Season.SPRING
            case 2:
                self.season = Season.SUMMER
            case 3:
                self.season = Season.FALL
        
        self.day_hrs, self.night_hrs = get_day_n_night_hrs_by_season(self.season)
        
    def calc_time_of_day(self):
        '''
        Sets self.time_of_day based on the current hour
        
        Nighttime is the beginning and end of the day
        Daytime is the the middle of the day
        
        '''
        if ((self.cur_hr >= 0 and self.cur_hr < self.night_hrs / 2)
            or self.cur_hr >= self.night_hrs / 2 + self.day_hrs
            ):
            self.time_of_day = TimeOfDay.NIGHT
        else:
            self.time_of_day = TimeOfDay.DAY
    
    def tick(self):
        self.cur_min += 1
        
        self.update_time()
        
    def tick_turn(self):
        self.cur_min += MINS_PER_TURN

        self.update_time()
            
    def update_time(self):
        
        self.cur_hr = self.cur_min % 60
        
        # check for a new day
        if self.cur_hr == HRS_IN_DAY:
            self.cur_min -= HRS_IN_DAY * 60
            self.cur_hr = 0
            self.days_passed += 1
        
        self.update_season()
            
        self.calc_time_of_day()
        
    
