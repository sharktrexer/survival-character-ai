from activity_mechanics.activities import Activity
from activity_mechanics.resources import ResourceManager
from activity_mechanics.time_management import TimeKeeper
from battle.battle_peep import BattlePeep

class Lodge:
    '''
    Info stored representing the state of the lodge
    '''
    def __init__(self, name, resourcer:ResourceManager):
        self.name = name
        self.resourcer = resourcer
        self.locations = []
        self.time_keeper = TimeKeeper()
        
    def do_activity(self, peep:BattlePeep, activity:Activity):
        
        #TODO: can the peep take the hunger hit?
        
        # can the peep take the stress hit!?   
        tres_effct = activity.stress_percent_cost * peep.value_of('tres')
        is_calm_enough = peep.points_of('tres') - tres_effct >= 0
        if not is_calm_enough:
            return False
        
        # resource exchange, if possible
        # MAKE SURE THIS IS THE LAST CHECK
        lodge_has_enough_resources = self.resourcer.exchange(activity.rescource_cost)
        if not lodge_has_enough_resources:
            return False
        
        # time goes by
        #TODO: what happens if ambushed!?
        self.time_keeper.tick_by_pip(activity.pips_req)
        
        # stat effects
        for chng in activity.stat_changes:
            peep.stats.grow_stat(chng.name, chng.val_amount, chng.apt_xp_amount)
            
        # stress resource effect
        peep.stats.resource_change("stress", tres_effct)
        
        # get resources produced, if possible
        #TODO: what if obtained vars is based on what happens in activity?
        self.resourcer.obtain(activity.produced_resc)
        