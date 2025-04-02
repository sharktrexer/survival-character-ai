from battle_peep import BattlePeep
from equations import do_gain_bonus_AP_from_init

class BattleManager():
    def __init__(self, members:list):
        self.rounds = 0
        self.members = members
        
    def get_anchor_init(self):
        anchor = min(self.members, key = lambda peep: peep.initiative())
        print("Anchor: " + anchor.name)
        return anchor.initiative()
    
    def change_member_list(self, peep:BattlePeep, do_add:bool):
        if do_add:
            self.members.append(peep)
        else:
            self.members.remove(peep)
            
        self.get_anchor_init()
        
    def next_round(self):
        self.rounds += 1
        
        for peep in self.members:
            do_gain_bonus_AP_from_init(peep, self.get_anchor_init())
            peep.turn()