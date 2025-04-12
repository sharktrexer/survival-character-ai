from battle_peep import BattlePeep

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
            self.do_gain_bonus_AP_from_init(peep, self.get_anchor_init())
            peep.turn()
            
    def do_gain_bonus_AP_from_init(self, peep: BattlePeep, anchor_init):

        self.get_anchor_init()
        
        peep.init_growth = (
            (peep.initiative() - anchor_init) * peep.init_rounds_passed ) 
        gain_bonus = peep.initiative() + peep.init_growth - anchor_init >= 2(anchor_init)
        # let peep know they have bonus
        if gain_bonus:
            peep.energy_bonus()
            
        return gain_bonus