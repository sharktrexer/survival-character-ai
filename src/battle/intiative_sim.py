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
    }),
    BattlePeep("Heavy Slime", {
        "strength": make_stat("str", 20, 2),
        "defense": make_stat("def", 20, 4),
        "evasion": make_stat("eva", 4, -3),
        "dexterity": make_stat("dex", 4, -3),
        "recovery": make_stat("rec", 10, 0),
        "intelligence": make_stat("int", 5, -4),
        "creativity": make_stat("cre", 5, -3,),
        "fear": make_stat("fear", 30, 3),
        "intimidation": make_stat("itmd", 10, 0),
        "charisma": make_stat("cha", 5, -4,),
        "stress": make_stat("tres", 50, 8),
        "health": make_stat("hp", 100, 4),
        "hunger": make_stat("hun", 20, 0),
        "energy": make_stat("ap", 10, 0),
    }),
    
]

PLAYGROUND = PEEPS + TEMP_ENEMIES

VALID_NAMES = [p.name for p in PLAYGROUND]

peep_test_group = PEEPS[0:3]

class InitiativeSimulator():
    
    def __init__(self):
        self.init_tester = BattleManager(peep_test_group)
    
    def start_round(self):
        print("~Intiative Sim~", "\n")
        print("Members:")
        for p in self.init_tester.members:
            
            print("[",p.name, "] with init: ", str(p.initiative()), sep="")
        self.init_tester.start_round()

    def modify_battle(self, peep_name, do_add):
        # validate name
        if peep_name in VALID_NAMES:
            # get peep by name
            peep = [p for p in PLAYGROUND if p.name == peep_name][0]
            self.init_tester.change_member_list(peep, do_add)
            return True
        else:
            print("Invalid peep name")
            return False
        
    def print_current_peeps(self):
        for p in self.init_tester.members:
            print("[",p.name, "] with init: ", str(p.initiative()))
            
    def print_options(self):
        for p in PLAYGROUND:
            print("[",p.name, "] with init: ", str(p.initiative()))