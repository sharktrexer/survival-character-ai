from battle.battle_manager import BattleManager
from battle.battle_peep import BattlePeep
from battle.stats import Stat, make_stat

from peep_data.data_reader import get_peeps


PEEPS = get_peeps()

TEMP_ENEMIES = [
    BattlePeep("Rat", {
        "strength": make_stat("str", 10, -2),
        "defense": make_stat("def", 10, 0),
        "evasion": make_stat("eva", 20, 4),
        "dexterity": make_stat("dex", 15, 2),
        "recovery": make_stat("rec", 10, 0),
        "intelligence": make_stat("int", 10, -1),
        "creativity": make_stat("cre", 8, -4,),
        "fear": make_stat("fear", 10, 0),
        "intimidation": make_stat("itmd", 10, -1),
        "charisma": make_stat("cha", 8, -2,),
        "stress": make_stat("tres", 10, 0),
        "health": make_stat("hp", 40, 0),
        "hunger": make_stat("hun", 20, -1),
        "energy": make_stat("ap", 8, 0),
    }),
    BattlePeep("Double Rat", {
        "strength": make_stat("str", 20, 0),
        "defense": make_stat("def", 10, 2),
        "evasion": make_stat("eva", 15, 2),
        "dexterity": make_stat("dex", 20, 2),
        "recovery": make_stat("rec", 10, 1),
        "intelligence": make_stat("int", 15, -1),
        "creativity": make_stat("cre", 10, -3,),
        "fear": make_stat("fear", 15, 1),
        "intimidation": make_stat("itmd", 10, 1),
        "charisma": make_stat("cha", 12, -2,),
        "stress": make_stat("tres", 10, -2),
        "health": make_stat("hp", 80, 1),
        "hunger": make_stat("hun", 20, -2),
        "energy": make_stat("ap", 10, 1),
    })
    
]



peep_test_group = PEEPS[0:3]

init_tester = BattleManager(peep_test_group)

def start_round():
    init_tester.next_round()