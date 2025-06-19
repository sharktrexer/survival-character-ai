from .battle_peep import BattlePeep

class BattleManager():
    def __init__(self, members:list):
        self.rounds = 0
        self.members = members
        self.init_anchor = self.get_anchor_init()
        
    def get_anchor_init(self):
        anchor = min(self.members, key = lambda peep: peep.initiative())
        print("Anchor: " + anchor.name, " with init: " + str(anchor.initiative()))
        return anchor.initiative()
    
    def change_member_list(self, peep:BattlePeep, do_add:bool):
        if do_add:
            print("Added " + peep.name)
            self.members.append(peep)
        else:
            print("Removed " + peep.name)
            self.members.remove(peep)
        
        self.init_anchor = self.get_anchor_init()
     
    def start_round(self):
        for peep in self.members:
            peep.start(self.init_anchor)
        
    def next_round(self):
        self.rounds += 1
        
        print("\n~Round " + str(self.rounds) + "~")
        
        print("\nCurrent Anchor Value: |" + str(self.init_anchor) + "|")
        print("Target: |" + str(self.init_anchor*2) + "|")
        
        for peep in self.members:
            self.do_gain_bonus_AP_from_init(peep)
            peep.turn()
            
    def do_gain_bonus_AP_from_init(self, peep: BattlePeep):
        
        """
        Calculates whether a peep should gain bonus AP based on their initiative 
        relative to the anchor's initiative.

        Parameters:
            peep (BattlePeep): the peep to check
            anchor_init (int): the anchor's initiative

        Returns:
            bool: whether the peep gained bonus AP
        """
        past_growth = peep.init_growth
        peep.init_growth += max(0, peep.initiative() - self.init_anchor)
        # max is used so there is never negative growth
            
#~~~~~~~~ Dont show growth if there is none
        if peep.initiative() == self.init_anchor:
            print(peep.name + " did not have growth as they are the anchor! :(")
            return False
#~~~~~~~~ Growth Calculation      
        else:         
            gain_bonus =  peep.init_growth >= 2 * self.init_anchor
            
            # print init growth
            print(peep.name + " - Growth: " + str(past_growth) + " -> " + str(peep.init_growth))
            
            # let peep know they have bonus
            if gain_bonus:
                peep.energy_bonus()
            
            return gain_bonus
    
