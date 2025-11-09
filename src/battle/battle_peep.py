import random
from .stats import Stat, StatBoard, sn
from .alteration import Alteration
from enum import Enum, auto
from .damage import Damage

''' A version of character that is battle oriented 
'''
class BattlePeep():
    def __init__(self, name: str, stats_dict: dict, move_set:list[int]=[0,1]):
        self.name = name
        self.stats = StatBoard(stats_dict)
        self.battle_handler = BattleHandler()
        self.init_growth = 0
        self.gained_ap_bonus = False
        self.is_player = False
        self.move_set = move_set
        self.team = None
        
    def __str__(self):
        return self.name
    
    def get_info_as_str(self):
        peep_info = self.name + ":\n"
        peep_info += self.stats.get_all_stats_as_str()
        return peep_info
    
    def get_label_as_str(self):
        standard_label = (f"{self.name}: "
                + f"{self.stats.get_stat_resource('hp')}/{self.stats.get_stat_active('hp')} HP"
                + f" {self.stats.get_stat_resource('ap')}/{self.stats.get_stat_active('ap')} AP")
        
        bleeding_label = (f"{self.name}: "
                + f"{self.battle_handler.bleed_out}/{self.battle_handler.bleed_out_max} Blood")
        
        dead_label = f"{self.name}:DEAD"
        
        if self.battle_handler.stance == Peep_State.BLEEDING_OUT:
            return bleeding_label
        elif self.battle_handler.stance == Peep_State.DEAD:
            return dead_label
        else:
            return standard_label
    
    def get_stat(self, name:str) -> Stat:
        '''
        given a name, returns the peep's current stat obj
        '''
        return self.stats.get_stat_cur(name)
    
    def get_all_stat_apts(self):
        return self.stats.get_all_stat_apts()
    
    def get_all_stat_avs(self):
        return self.stats.get_all_stat_active_value
     
    def initiative(self):
        '''
        Returns:
            Combined active values of Dexterity and Evasion
        '''
        return self.stats.initiative()
    
    def recieve_alt(self, alt: Alteration):
        self.stats.apply_alteration(alt)
        
    def cleanse_alt(self, alt: Alteration):
        self.stats.remove_alteration(alt)
        
    def start(self):
        '''
        Lets this peep start their turn
        '''
        #TODO: Add start logic
        # trigger all on start turn effects

            
        
        pass 
    
    def turn(self):
        if self.battle_handler.stance == Peep_State.DEAD:
            return
        
        # are we bleeding out?
        if self.battle_handler.handle_bleeding_out():
            #TODO: what happens when we dead for reals?
            print(f"{self.name} bled out!")
            return
        
        # time has passed for alterations
        self.stats.tick_alterations()
        
        if self.battle_handler.stance == Peep_State.BLEEDING_OUT:
            #TODO: extra logic for knocked out peeps
            # currently will ignore energy bonus 
            # could ignore getting input from ai or player
            # perhaps trigger a flag to "help me!" and attract NPCs to help
            
            return
        
        # ap roll over, leftover ap below or equal to 50% of max ap is rolled over
        rollover = min(self.stats.get_stat_active("ap") // 2, 
                      self.stats.get_stat_resource("ap"))
        
        # apply energy bonus
        if self.gained_ap_bonus: self.stats.apply_init_ap_bonus()
        
        # restore ap value
        self.stats.resource_restore("ap")
        
        # apply rollover
        self.stats.resource_change_uncapped("ap", rollover)


    def end_turn(self):
        # revert energy bonus
        self.gained_ap_bonus = False
    
    def end_battle(self):
        # recover wih 10% health if knocked out at end of battle
        if self.battle_handler.stance == Peep_State.BLEEDING_OUT: 
            self.recover_from_battle_end()
        
        # let battle handler know    
        self.battle_handler.end_battle()   
        
        
    def affect_hp(self, affect:Damage):
        amount = affect.amount
        
        if self.battle_handler.stance == Peep_State.DEAD:
            return
        
        # when bleeding out
        if self.stats.resource_is_depleted('hp'): 
            
            past_bleed_out = self.battle_handler.bleed_out
            
            self.battle_handler.affect_bleed_out(amount)
            '''
            If bleed out hp >= max hp then set current hp equal to overflow from max_hp (minimum 1)
            '''
            if amount > 0 and self.battle_handler.bleed_out >= self.battle_handler.bleed_out_max:
                restored_hp = past_bleed_out + amount - self.battle_handler.bleed_out_max + 1
                self.stats.resource_change('hp', restored_hp)
                self.battle_handler.stance = Peep_State.STANDARD
            
            return
        
        resisting_stat_amnt = 0
        # get stat to resist against damage
        if not affect.is_heal:
            amnt_before = amount
            resisting_stat_amnt = self.stats.get_stat_active(affect.resisting_stat)
            resisting_stat_amnt /= 4
            amount += resisting_stat_amnt
            # don't let resisting damage heal!
            if amount > 0:
                amount = -1
            print(f"| Resisted! {amnt_before} -> {amount}", end="")
        
        # apply damage   
        depleted = self.stats.resource_change('hp', amount)
        
        # knock out
        if depleted:
            self.battle_handler.start_bleeding_out(self.stats.get_stat_cur('hp').val_active)
            print(f"\n{self.name} has been knocked out!")
            self.init_growth = 0
            # TODO: affect fear and/or stress. maybe hunger too?
            
    def recover_from_battle_end(self):
        self.stats.resource_set_to_percent('hp', 0.1)
        #TODO: is anything else needed?
 
 
class Peep_State(Enum):
    STANDARD = auto()
    FLYING = auto()
    PRONE = auto()
    HANGING = auto()
    BLEEDING_OUT = auto()
    KNOCKED_DOWN = auto()
    DEAD = auto()
        
'''
    Is a part of a battle peep to store and manipulate extra situational info
''' 
class BattleHandler():
    def __init__(self):
        self.temp_health:int = 0
        self.defense_health:int = 0
        self.evasion_health:int = 0
        self.bleed_out:int = 0
        self.bleed_out_max:int = 0
        self.times_knocked_down:int = 0
        self.status_effects = []
        self.stance = Peep_State.STANDARD
        
    def start_bleeding_out(self, max_hp:int):
        '''
        Let BattleHandler know that peep is knocked out
        
        Args:
            max_hp (int): max hp of peep to represent bleed out health
        '''
        self.defense_health = 0
        
        self.stance = Peep_State.BLEEDING_OUT
        self.bleed_out_max = max_hp 
        
        # calculate bleed out trauma
        # reduces by 25% for each knock out, minimum 1
        self.bleed_out = max(1, int(max_hp * (1 - 0.25 * self.times_knocked_down)))
        
        self.times_knocked_down += 1
        
    def handle_bleeding_out(self):
        '''
        Called every battlepeep's turn to check if they are bleeding out
        and dealing with the logic of bleeding out
        
        Returns:
            bool: if peep is dead from bleeding out
        '''
        if self.stance != Peep_State.BLEEDING_OUT:
            return False
        
        temp = self.bleed_out
        self.bleed_out = int(self.bleed_out - self.bleed_out_max * 0.1)
        print(f"bleed out: {temp} -> {self.bleed_out}")
        
        if self.bleed_out <= 0:
            self.die()
            
            return True
        
        return False
    
    def affect_bleed_out(self, amount:int):
        '''        
        when recieving damage: reduce by 80%. 
        If bleed out hp <= 0 then die
        '''
        # Should peep's stats or magic resist matter?
        amount = amount if amount > 0 else int(amount * 0.2)
        
        temp = self.bleed_out
        self.bleed_out += amount
        #print(f"\nrecieved dmg while bleeding: {temp} -> {self.bleed_out}")
        
        if self.bleed_out > self.bleed_out_max:
            self.bleed_out = self.bleed_out_max
        elif self.bleed_out <= 0:
            self.bleed_out = 0
            self.die()
            
    def die(self):
        self.stance = Peep_State.DEAD
        self.times_knocked_down = 0
        print(f"died!")
        
    def end_battle(self):
        # perhaps stance could be different if char is always flying
        self.stance = Peep_State.STANDARD
        self.bleed_out = 0
        self.bleed_out_max = 0
        self.evasion_health = 0
        self.defense_health = 0
        self.times_knocked_down = 0
        # temp hp can potentially carry over out of battle
        
class Inventory():
    
    def __init__(self):
        self.equipped = []
        self.carrying = []
        
    def sort(self):
        pass
    
    def equip(self):
        pass
        
    def unequip(self):
        pass
    
    def add_item(self):
        pass
    
    def remove_item(self):
        pass
        
    