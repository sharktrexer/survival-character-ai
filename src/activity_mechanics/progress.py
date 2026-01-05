from activity_mechanics.activities import Activity


MIN_PROG_FOR_GRACE = 0.20

class PeepProgress():
    def __init__(self, name:str, starting_pip:int= 0):
        self.name = name
        self.starting_pip = starting_pip
        
class ActivityProgress():
    def __init__(self, peep_progs:list[PeepProgress], Activity:Activity):
        self.peep_progs = peep_progs
        self.activity = Activity
        self.pip_prog = 0
        
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
        progress = 0
        
        if round(self.pip_prog / self.pips_req_to_finish(), 2 ) > MIN_PROG_FOR_GRACE:
            progress = self.pip_prog
        
        self.peep_progs.append(PeepProgress(name, progress))
        
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