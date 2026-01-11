from activity_mechanics.progress import ActivityProgress, Activity, PeepProgress
from battle.stats import StatChange

test_choices = ['work hard! >:)', "chill out B)"]

class ActivityManager:
    def __init__(self):
        self.in_prog_activities: list[ActivityProgress] = []
    
    def get_activites_by_name(self, name:str):
        return [a for a in self.in_prog_activities if a.activity.name == name]
    
    def get_activites_by_room(self, room_name:str):
        return [a for a in self.in_prog_activities if a.activity.location == room_name]
    
    def add_activity(self, peep_name:str, activity:Activity):
        self.in_prog_activities.append(
            ActivityProgress(
                [PeepProgress(peep_name)], 
                activity
                )
            )
        
    def add_peep_to_activity(self, peep_name:str, act_progress:ActivityProgress):
        act_progress.join_group(peep_name)
        
    def start_tick(self, act_progress:ActivityProgress):
        act_progress.tick()
        
        # test random event
        if act_progress.pip_prog == 5:
            return test_choices
        #TODO: grab even list based on the activity or other conditions
        
    
    def finish_tick(self, act_progress:ActivityProgress, choice_ind:int):
        
        if choice_ind >= len(test_choices) or choice_ind < 0:
            return
        
        # take index and make sense of it
        # work hard
        if choice_ind == 0:
            for s_chng in act_progress.activity.stat_changes:
                if s_chng.val_amount > 0:
                    s_chng.val_amount += 1
            act_progress.activity.gauge_costs.append(StatChange("tres", -10))
        else:
            # work soft
            act_progress.activity.gauge_costs.append(StatChange("tres", 5))
            
    def clean_activity_list(self):
        '''
        Removes finished activities from list
        '''
        self.in_prog_activities = [a for a in self.in_prog_activities if not a.is_finished()]
        