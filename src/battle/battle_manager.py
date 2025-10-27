from .battle_peep import BattlePeep, Attack

class BattleManager():
    def __init__(self, members:list[BattlePeep]):
        self.rounds = 0
        self.members = members
        self.init_anchor = 0
        
    def get_anchor_init(self):
        """ 
        Sets the anchor initiative value to the lowest initiative value among the 
        peeps. The anchor value is used to determine when a peep gains 
        bonus AP. 
        
        The anchor should update when:
        1. The fight begins
        2. The end of a round (takes into account those who left, joined, knocked out)
        """
        if self.members == []: return 0
        
        valid_members = [peep for peep in self.members if not peep.stats.resource_is_depleted('hp')]
        if valid_members == []: return 0
        
        anchor = min(valid_members, key = lambda peep: peep.initiative())
        print("Anchor: " + anchor.name + " with init: " + str(anchor.initiative()))
        self.init_anchor = anchor.initiative()
    
    def get_member_names(self):
        return [peep.name for peep in self.members]
    
    def change_member_list(self, peep:BattlePeep, do_add:bool):
        if do_add:
            print("Added " + peep.name)
            self.members.append(peep)
        else:
            print("Removed " + peep.name)
            self.members.remove(peep)
        
        #self.get_anchor_init()
     
    def start_round(self):
        self.get_anchor_init()
        
        #TODO: Does this need to be in order of initiative?
        for peep in self.members:
            peep.start()
        
    def next_round(self):
        self.rounds += 1
        
        print("\n~Round " + str(self.rounds) + "~")
        
        #print("\nCurrent Anchor Value: |" + str(self.init_anchor) + "|")
        #print("Target: |" + str(self.init_anchor*2) + "|")
        
        
        
        # order peep turns by initiative
        for peep in sorted(self.members, key = lambda peep: peep.initiative(), reverse=True):
            
            print()
            print(peep.get_label_as_str())
            
            # calc growth if unit is alive
            if not peep.stats.resource_is_depleted('hp'): 
                self.do_gain_bonus_AP_from_init(peep)
            
            cur_move:Attack = peep.turn(self.members)
            # skip turn of no move
            if cur_move is None:
                continue
            
            value = cur_move.get_value(peep.stats.get_stat_cur(cur_move.stat).val_active)
            print(f'{peep.name} used {cur_move.name} for {value}' 
                  + f' on {cur_move.target_names[0]}', end=" ")
            
            # get target by provided name
            target:BattlePeep = None
            for member in self.members:
                if member.name == cur_move.target_names[0]:
                    target = member
                    break
            value = value if cur_move.is_heal else -value
            target.affect_hp(value)
            
            # printing move effect
            if not target.stats.resource_is_depleted('hp'):
                print(f'({target.name} = {target.stats.get_stat_cur("hp").val_resource}/{target.stats.get_stat_cur("hp").val_active} HP)')
            else:
                print(f'({target.name} = {target.battle_handler.bleed_out}/{target.battle_handler.bleed_out_max} Bleed)')
            
            peep.end_turn()
            
        # update anchor after round
        self.get_anchor_init()
            
            
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
            #print(peep.name + " did not have growth as they are the anchor! :(")
            return False
#~~~~~~~~ Growth Calculation      
        else:         
            do_gain_bonus =  peep.init_growth >= 2 * self.init_anchor
            
            # print init growth
            #print(peep.name + " - Growth: " + str(past_growth) + " -> " + str(peep.init_growth))
            
            # let peep know they have bonus
            if do_gain_bonus:
                #print(peep.name + " - Gained energy bonus from initiative! Growth reset :O")
                peep.init_growth = 0
                peep.gained_ap_bonus = True
            
            return do_gain_bonus
    

   