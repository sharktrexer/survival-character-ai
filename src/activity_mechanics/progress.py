from activity_mechanics.activities import Activity


MIN_PROG_FOR_GRACE = 0.20

class PeepProgress():
    def __init__(self, name:str, starting_pip:int= 0):
        self.name = name
        self.starting_pip = starting_pip
        
    def __str__(self):
        return f'{self.name}, started at {self.starting_pip}'
        
class ActivityProgress():
    def __init__(self, peep_progs:list[PeepProgress], Activity:Activity):
        self.peep_progs = peep_progs
        self.activity = Activity
        self.pip_prog = 0
    
    def __str__(self):
        names = ', '.join([peep.name for peep in self.peep_progs])
        return f'{names} - {self.pip_prog}/{self.pips_req_to_finish()}'
    
    def __repr__(self):
        return self.__str__()
    
    def get_all_peep_names(self):
        return [peep.name for peep in self.peep_progs]
    
    def get_group_size(self):
        return len(self.peep_progs)
        
    def is_solo(self):
        return len(self.peep_progs) == 1
    
    def is_group(self):
        return len(self.peep_progs) > 1
    
    def is_finished(self):
        return self.pip_prog >= self.pips_req_to_finish()
    
    def pips_req_to_finish(self):
        return self.activity.time_pip_cost
    
    def join_group(self, name:str):
        '''
        Adds a new peep to the group
        Their starting progress will reflect how late the joined the group
        If progress is not too much, lateness will be ignored
        '''
        startin_prog = 0
        prog_percent = round(self.pip_prog / self.pips_req_to_finish(), 2 )
        if prog_percent > MIN_PROG_FOR_GRACE:
            startin_prog = self.pip_prog
        
        self.peep_progs.append(PeepProgress(name, startin_prog))
        
    def tick(self):
        self.pip_prog += 1
        self.get_tick_bonus()
        return self.is_finished()
    
    def get_tick_bonus(self):
        '''
        Calculates the extra bonus pip progress
        '''
        bonus = 0
        # there is multiple people working on the activity
        # grant bonus prog every X completed pips
        if self.pip_prog % 5 == 0 and self.is_group():
            bonus += 1
            
        self.pip_prog += bonus