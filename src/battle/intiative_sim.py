from battle_manager import BattleManager
from battle_peep import BattlePeep
from peep.char_data import PEOPLE

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Initiative Sim Chars~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

chris = BattlePeep(PEOPLE[0].name, PEOPLE[0].desc, PEOPLE[0].stat_aps)
adan = BattlePeep(PEOPLE[1].name, PEOPLE[1].desc, PEOPLE[1].stat_aps)
mudman = BattlePeep("Mud Man", "Very muddy...", {
                "Strength": 0, "Defense": 0, "Evasion":-2,
                "Dexterity": -2, "Recovery": 0, "Intellect": 0,
                "Creativity": 0, "Fear": 0, "Intimidation": 0,
                "Charisma": 0, "Stress": 0, "Health":0,
                "Hunger": 0, "Energy": 0
                })
fairy = BattlePeep("Fairy", "Sparkels!", {
                "Strength": 0, "Defense": 0, "Evasion":7,
                "Dexterity": 7, "Recovery": 0, "Intellect": 0,
                "Creativity": 0, "Fear": 0, "Intimidation": 0,
                "Charisma": 0, "Stress": 0, "Health":0,
                "Hunger": 0, "Energy": 0
                },
                {
                "Strength": 10, "Defense": 10, "Evasion":20,
                "Dexterity": 30, "Recovery": 0, "Intellect": 0,
                "Creativity": 0, "Fear": 0, "Intimidation": 0,
                "Charisma": 0, "Stress": 0, "Health":0,
                "Hunger": 0, "Energy": 0
                })


init_tester = BattleManager([])