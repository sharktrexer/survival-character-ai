from battle.battle_peep import BattlePeep
from battle.stats import StatBoard, Stat, make_stat
from battle.damage import Damage
from peep_data.data_reader import PEEPS

import copy

EON = BattlePeep("", {
    "strength": make_stat("str", 9999, 8),
    "defense": make_stat("def", 9999, 8),
    "evasion": make_stat("eva", 9999, 8),
    "dexterity": make_stat("dex", 9999, 8),
    "recovery": make_stat("rec", 9999, 8),
    "intelligence": make_stat("int", 9999, 8),
    "creativity": make_stat("cre", 9999, 8),
    "fear": make_stat("fear", 9999, 8),
    "intimidation": make_stat("itmd", 9999, 8),
    "charisma": make_stat("cha", 9999, 8),
    "stress": make_stat("tres", 9999, 8),
    "health": make_stat("hp", 9999, 8),
    "hunger": make_stat("hun", 9999, 8),
    "energy": make_stat("ap", 9999, 8),
})

class PeepManager:
    
    @staticmethod
    def reset_stat_to_default(peep:BattlePeep, stat:Stat):
        default_stat = PEEPS[peep.name].get_stat(stat.name)
        stat.set_new_vals_as_reset(default_stat.value, default_stat.apt)
        
    @staticmethod
    def reset_peep_to_default(peep:BattlePeep):
        peep = copy.deepcopy([p for p in PEEPS if p.name == peep.name][0])
    
    @staticmethod    
    def kill_peep(peep:BattlePeep):
        the_kill = Damage(1,'str','hun')
        the_kill.give_value(EON.value_of('hun'))
        peep.affect_hp(the_kill, attacker=EON)
