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

# Constants
MINS_PER_PIP = 10
MINS_PER_HR = 60    
PIPS_PER_TURN = 1
PIPS_PER_HR = 60 // MINS_PER_PIP

HRS_IN_DAY = 24
NUM_OF_SEASONS = 4
DAYS_PER_SEASON = 5
DAYS_PER_YEAR = 25

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
    
    def __str__(self):
        return f'''
        Day {self.days_passed}, {self.time_of_day.name.lower()}time |
         Time: {self.get_time_formatted()}
         Season: {self.season.name[0].upper() + self.season.name[1:].lower()}'''
    
    def get_time_formatted(self):
        hour = self.cur_hr
        if self.cur_hr < 10:
            hour =  f"0{self.cur_hr}"
            
        minute = self.cur_min
        if self.cur_min < 10:
            minute =  f"0{self.cur_min}"    
            
        return f"{hour}:{min}"
        
    
    def cur_year(self):
        return self.days_passed // DAYS_PER_YEAR
    
    def update_season(self):
        '''
        ### every 5 days change season 
        #   5   -   5   -   5   - 5
        ### Winter, Spring, Summer, Fall
                 4 seasons
            ##    /_________\\
        25 Days in the 'Year'
        4 years in 100 days
        '''
        season_input = (self.days_passed // DAYS_PER_SEASON) % NUM_OF_SEASONS
            
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
        # declares night as the first and last hours of the day
        if ((self.cur_hr >= 0 and self.cur_hr < self.night_hrs / 2)
            or (self.cur_hr >= self.night_hrs / 2 + self.day_hrs)
            ):
            self.time_of_day = TimeOfDay.NIGHT
        else:
            self.time_of_day = TimeOfDay.DAY
    
    def tick(self):
        self.tick_by_pip(1)

    def tick_turn(self):
        self.tick_by_pip(PIPS_PER_TURN)
        
    def tick_by_pip(self, pips:int):
        self.cur_min += pips * MINS_PER_PIP
        
        self.update_time()
            
    def update_time(self):
        
        self.cur_hr = self.cur_min % MINS_PER_HR
        
        # check for a new day
        if self.cur_hr >= HRS_IN_DAY:
            self.cur_min -= HRS_IN_DAY * MINS_PER_HR
            self.cur_hr = self.cur_min % MINS_PER_HR
            self.days_passed += 1
        
        self.update_season()
            
        self.calc_time_of_day()
        
    
