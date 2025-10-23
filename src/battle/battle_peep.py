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
        peep_info += self.stats.get_stats_as_str()
        return peep_info
    
    def get_stat(self, name:str) -> Stat:
        '''
        given a name, returns the peep's current stat obj
        '''
        return self.stats.get_stat_cur(name)
    
    def get_stat_apts(self):
        return self.stats.get_stat_apts()
    
    def get_stat_avs(self):
        return self.stats.get_stat_active_value
     
    def initiative(self):
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
            print(f"{self.name} was knocked out!")
            return
        
        # apply energy bonus
        if self.gained_ap_bonus: self.stats.apply_init_ap_bonus()
        
        # restore ap value
        self.stats.resource_restore("ap")
        
        '''~~~~~~~~~~~~~~~~~~~~~~~~MOVES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
        
        allies = [battler for battler in battlers if battler.team == self.team]
        enemies = [battler for battler in battlers if battler.team != self.team]
        
        allies_max_hp = sum([ally.stats.get_stat_cur("hp").val_active for ally in allies])
        allies_cur_hp = sum([ally.stats.get_stat_cur("hp").val_resource for ally in allies])
        allies_hp_ratio = allies_cur_hp / allies_max_hp
        
        move_choice = 0
        
        if allies_hp_ratio > 0.5:
            move_choice = 0
        else:
            move_choice = 1
            
        
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
        if self.stats.resource_is_depleted('hp'): 
            #TODO: logic for affecting bleed out health when taking dmg
            
            # affect bleed out
            '''
            when healed: increase bleed out. If bleed out hp >= max hp then set current hp equal to 
            overflow from max_hp (minimum 1)
            
            when recieving damage: reduce by 80%. If bleed out hp <= 0 then die
            '''
            self.battle_handler.affect_bleed_out(amount)
            
            return
        
        # TODO: get the type of damage (using STR, DEX, etc.) and use the opposing
        # stat to resist it
        depleted = self.stats.resource_change('hp', amount)
        
        # knock out
        if depleted:
            self.battle_handler.knock_out(self.stats.get_stat_cur('hp').val_active)
            print(f"{self.name} has been knocked out!")
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
        self.temp_health = 0
        self.evasion_health = 0
        self.bleed_out = 0
        self.bleed_out_max = 0
        self.times_knocked_down = 0
        self.status_effects = []
        self.stance = Peep_State.STANDARD
        
    def knock_out(self, max_hp:int):
        '''
        Let BattleHandler know that peep is knocked out
        
        Args:
            max_hp (int): max hp of peep to double to represent bleed out health
        '''
        self.stance = Peep_State.KNOCKED_OUT
        self.bleed_out = max_hp
        self.bleed_out_max = max_hp
        self.times_knocked_down += 1
        
        # if knocked down too many times, die lol
        if self.times_knocked_down > 3:
            self.die()
        
    def handle_bleeding_out(self):
        '''
        Called every battlepeep's turn to check if they are bleeding out
        and dealing with the logic of bleeding out
        
        Returns:
            bool: if peep is dead from bleeding out
        '''
        if self.stance != Peep_State.KNOCKED_OUT:
            return
        
        # TODO: count down bleed out based on HP Apt
        # 5 rounds for Apt 0, 15 at Apt 8, 3 for Apt -4
        temp = self.bleed_out
        self.bleed_out -= self.bleed_out_max  * 0.1
        print(f"bleed out: {temp} -> {self.bleed_out}")
        if self.bleed_out <= 0:
            self.die()
            
            return True
        
        return False
    
    def affect_bleed_out(self, amount:int):
        '''
        Affect bleed out health by amount
        Amount if 80% less effective if it speeds up the bleed out process
        '''
        amount = amount if amount > 0 else amount * 0.8
        
        temp = self.bleed_out
        self.bleed_out += amount
        print(f"recived dmg while bleeding: {temp} -> {self.bleed_out}")
        if self.bleed_out > self.bleed_out_max:
            self.bleed_out = self.bleed_out_max
        elif self.bleed_out <= 0:
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
        
    