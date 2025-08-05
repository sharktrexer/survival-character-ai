from battle.battle_peep import BattlePeep
from battle.stats import StatBoard, Stat
from peep_data.data_reader import PEEPS

import copy


class PeepManager:
    
    @staticmethod
    def reset_stat_to_default(peep:BattlePeep, stat:Stat):
        default_stat = PEEPS[peep.name].get_stat(stat.name)
        stat.set_new_vals_as_reset(default_stat.value, default_stat.apt)
        
    def reset_peep_to_default(peep:BattlePeep):
        peep = copy.deepcopy(PEEPS[peep.name])
