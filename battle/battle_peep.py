from peep.character import Character

''' A version of character that can be used in battle '''
class BattlePeep(Character):
    def __init__(self, name: str, desc: str, stats_dict: dict):
        super().__init__(name, desc, stats_dict)
        self.init_bonus = 0
        self.rounds_passed = 0
        