from .battle_manager import BattleManager
from .battle_peep import BattlePeep

import peep_data.data_reader as dr

dr.read_peep_data()

PEEPS = dr.get_peeps()

peep_test_group = PEEPS[0:3]


init_tester = BattleManager(peep_test_group)

def start_round():
    init_tester.next_round()