import random
from .stats import Stat, StatBoard, sn
from .alteration import Alteration
from enum import Enum, auto
from .attack import Attack

''' A version of character that is battle oriented 
'''
class BattlePeep():
    def __init__(self, name: str, stats_dict: dict, move_set:list[Attack]=[]):
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
        
        if self.battle_handler.stance == Peep_State.KNOCKED_OUT:
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
    
    def turn(self, battlers:list[BattlePeep]) -> Attack:
        if self.battle_handler.stance == Peep_State.DEAD:
            return
        
        # are we bleeding out?
        if self.battle_handler.handle_bleeding_out():
            #TODO: what happens when we dead for reals?
            print(f"{self.name} bled out!")
            return
        
        # time has passed for alterations
        self.stats.tick_alterations()
        
        if self.battle_handler.stance == Peep_State.KNOCKED_OUT:
            #TODO: extra logic for knocked out peeps
            # currently will ignore energy bonus 
            # could ignore getting input from ai or player
            # perhaps trigger a flag to "help me!" and attract NPCs to help
            
            return
        
        # apply energy bonus
        if self.gained_ap_bonus: self.stats.apply_init_ap_bonus()
        
        # restore ap value
        self.stats.resource_restore("ap")
        
        '''~~~~~~~~~~~~~~~~~~~~~~~~MOVES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
        
        allies = [battler for battler in battlers if battler.team == self.team]
        enemies = [battler for battler in battlers if battler.team != self.team]
        
        allies_max_hp = sum([ally.stats.get_stat_active("hp") for ally in allies])
        allies_cur_hp = sum([ally.stats.get_stat_resource("hp") for ally in allies])
        dead_affect = sum([int(ally.battle_handler.stance == Peep_State.KNOCKED_OUT) * 0.2 for ally in allies])
        
        allies_hp_ratio = (allies_cur_hp / allies_max_hp) - dead_affect
        
        move_choice = 0
        
        # more chance to heal when teammates are hurtin
        if allies_hp_ratio > 0.5:
            rand = random.randint(0, 100)
            if rand > 10:
                move_choice = 0
            else:
                move_choice = 1
        else:
            rand = random.randint(0, 100)
            if rand > 10:
                move_choice = 1
            else:
                move_choice = 0
            
        
        move = self.move_set[move_choice]
        targets:list[BattlePeep] = []
        # get target
        if move.is_for_team:
            targets = allies
        else:
            targets = enemies
            
        the_target = targets[random.randint(0, len(targets) - 1)]
        move.target_names = [the_target.name]
        return move
     
     
    def end_turn(self):
        # revert energy bonus
        self.gained_ap_bonus = False
    
    def end_battle(self):
        # recover wih 10% health if knocked out at end of battle
        if self.battle_handler.stance == Peep_State.KNOCKED_OUT: 
            self.recover_from_battle_end()
        
        # let battle handler know    
        self.battle_handler.end_battle()   
        
        
    def affect_hp(self, amount:int):
        
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
        
        # TODO: get the type of damage (using STR, DEX, etc.) and use the opposing
        # stat to resist it
        depleted = self.stats.resource_change('hp', amount)
        
        # knock out
        if depleted:
            self.battle_handler.knock_out(self.stats.get_stat_cur('hp').val_active)
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
    KNOCKED_OUT = auto()
    DEAD = auto()
        
'''
    Is a part of a battle peep to store and manipulate extra situational info
''' 
class BattleHandler():
    def __init__(self):
        self.temp_health:int = 0
        self.evasion_health:int = 0
        self.bleed_out:int = 0
        self.bleed_out_max:int = 0
        self.times_knocked_down:int = 0
        self.status_effects = []
        self.stance = Peep_State.STANDARD
        
    def knock_out(self, max_hp:int):
        '''
        Let BattleHandler know that peep is knocked out
        
        Args:
            max_hp (int): max hp of peep to represent bleed out health
        '''
        self.stance = Peep_State.KNOCKED_OUT
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
        if self.stance != Peep_State.KNOCKED_OUT:
            return False
        
        # TODO: count down bleed out based on HP Apt
        # 5 rounds for Apt 0, 15 at Apt 8, 3 for Apt -4
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
        
    