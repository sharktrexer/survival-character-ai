import random
from .stats import Stat, StatBoard, sn, GAUGE_STATS
from .alteration import Alteration
from enum import Enum, auto
from .damage import Damage

BATTLE_STATS = [
    'dodge', 'blood', 'armor', 'temp'
]

''' A version of character that is battle oriented 
'''
class BattlePeep():
    def __init__(self, name: str, stats_dict: dict):
        self.name = name.replace('_', ' ')
        self.key_name = name
        self.stats = StatBoard(stats_dict)
        self.battle_handler = BattleHandler()
        self.init_growth = 0
        self.gained_ap_bonus = False
        self.is_player = False
        self.team = None
        self.turns_passed = 0
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"{self.key_name}, team={self.team}, stats_dict={self.stats.__dict__}, )"
    
    def get_info_as_str(self):
        peep_info = self.name + ":\n"
        peep_info += self.stats.get_all_stats_as_str()
        return peep_info
    
    def get_label_as_str(self):
        standard_label = (f"{self.name}: "
                + f"{self.points_of('hp')}/{self.value_of('hp')} HP"
                + f" {self.points_of('ap')}/{self.value_of('ap')} AP")
        
        # addon evasion points
        if self.battle_handler.evasion_health > 0:
            standard_label += f"! {self.battle_handler.evasion_health} EvaP"
            
        # addon defense points
        if self.battle_handler.defense_health > 0:
            standard_label += f"! {self.battle_handler.defense_health} DefP"
        
        bleeding_label = (f"{self.name}: "
                + f"{self.battle_handler.bleed_out}/{self.battle_handler.bleed_out_max} Blood")
        
        dead_label = f"{self.name}:DEAD"
        
        if self.stance() == Peep_State.BLEEDING_OUT:
            return bleeding_label
        elif self.stance() == Peep_State.DEAD:
            return dead_label
        else:
            return standard_label
    
    def get_stat(self, name:str) -> Stat:
        '''
        given a name, returns the peep's current stat obj
        '''
        return self.stats.get_stat_cur(name)
    
    def stance(self):
        '''
        This peep's PeepState
        '''
        return self.battle_handler.stance
    
    def dodge(self):
        '''
        This peep's evasion health
        '''
        return self.battle_handler.evasion_health
    
    def armor(self):
        '''
        This peep's defense health
        '''
        return self.battle_handler.defense_health
    
    def blood(self):
        '''
        This peep's bleed out health
        '''
        return self.battle_handler.bleed_out
    
    def max_blood(self):
        '''
        This peep's bleed out max health
        '''
        return self.battle_handler.bleed_out_max
    
    def health(self):
        '''
        This peep's current health value
        '''
        return self.points_of('hp')
    
    def fear(self):
        '''
        This peep's current fear value
        '''
        return self.points_of('fear')
    
    def stress(self):
        '''
        This peep's current stress value
        '''
        return self.points_of('tres')

    def hunger(self):
        '''
        This peep's current hunger value
        '''
        return self.points_of('hun')
    
    def energy(self):
        '''
        This peep's current energy value
        '''
        return self.points_of('ap')
    
    def points_of(self, name:str):
        '''
        Get the resource value of a stat
        Or any Battle Health available
        '''
        match name:
            case 'dodge':
                return self.dodge()
            case 'armor':
                return self.armor()
            case 'blood':
                return self.blood()
            case 'temp':
                return self.battle_handler.temp_health
        
        return self.stats.get_stat_resource(sn(name))
    
    def value_of(self, stat_name:str):
        '''
        Get the active value of a stat
        '''
        if stat_name == 'blood':
            return self.max_blood()
        return self.stats.get_stat_active(sn(stat_name))
    
    def apt_of(self, stat_name:str):
        return self.stats.get_stat_apt(sn(stat_name))
    
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
        # reduce debuff effectiveness depending on how high hunger resource is
        self.stats.apply_alteration(alt)
        
    def cleanse_alt(self, alt: Alteration):
        self.stats.remove_alteration(alt)
        
    def start(self):
        '''
        Lets the peep know combat has starte
        '''
        #TODO: Add start logic
        # trigger all on start turn effects

        # Start with evasion health with high eva apt
        #TODO: should be a choice to use AP to get the evaP
        evasion = self.stats.get_stat_cur("eva")
        if evasion.apt >= 4:
            self.change_evasion_health(evasion.val_active // 3)    
        
    def start_turn(self):
        # Evasion health decays when turn begins (excluding starting evasion)
        if self.turns_passed != 0:
            self.battle_handler.evasion_health = 0
        
        if self.stance() == Peep_State.DEAD:
            return
        
        # are we bleeding out?
        if self.battle_handler.handle_bleeding_out():
            #TODO: what happens when we dead for reals?
            print(f"{self.name} bled out!")
            return
        
        # time has passed for alterations
        self.stats.tick_alterations()
        
        if self.stance() == Peep_State.BLEEDING_OUT:
            #TODO: extra logic for knocked out peeps
            # currently will ignore energy bonus 
            # could ignore getting input from ai or player
            # perhaps trigger a flag to "help me!" and attract NPCs to help
            
            return
        
        # ap roll over, leftover ap below or equal to 50% of max ap is rolled over
        rollover = 0
        if self.turns_passed > 0:
            rollover = min(self.value_of("ap") // 2, 
                        self.points_of("ap"))
        
        # apply energy bonus
        if self.gained_ap_bonus: self.stats.apply_init_ap_bonus()
        
        # restore ap value
        self.stats.resource_restore("ap")
        
        # apply rollover
        self.stats.resource_change_uncapped("ap", rollover)
        
        #self.handle_knock_down()


    def handle_knock_down(self):
        '''lose 25% of ap to get up from knocked down state'''
        if self.stance() == Peep_State.KNOCKED_DOWN:
            cur_ap = self.points_of("ap")
            self.stats.resource_change('ap', -(cur_ap // 4))
            self.change_state(Peep_State.STANDARD)
    
    def end_turn(self):
        # revert energy bonus
        self.gained_ap_bonus = False
    
    def end_battle(self):
        # recover wih 10% health if knocked out at end of battle
        if self.stance() == Peep_State.BLEEDING_OUT: 
            self.recover_from_battle_end()
        
        # let battle handler know    
        self.battle_handler.end_battle()   
        
    def try_to_evade(self, attacker:BattlePeep):
        '''
        Returns:
            If attack is dodged
        '''
        if self.battle_handler.evasion_health <= 0:
            return False
        
        # deal with evasion health
        #TODO: decide if this peep wants to evade
        evade_hp_dmg = attacker.value_of('dex') * -1
        past_evade_hp = self.battle_handler.evasion_health
        
        self.change_evasion_health(evade_hp_dmg)
        
        if past_evade_hp + evade_hp_dmg >= 0:
            # ignore attack if evasion health fully absorbed attack
            #print(f"EVADED!", end=" ")
            return True
        
        return False
        
    def change_state(self, state:Peep_State):
        self.battle_handler.stance = state 
    
    def affect_fear(self, affect:Damage, attacker:BattlePeep):
        
        amount = affect.amount
        
        # When healing stress, 25% of attacker's rec is added
        if affect.is_heal:
            amount += (attacker.value_of('rec') // 4)
        # If taking fear damage, 25% of self tres is used to resist
        else:
            amount -= (self.value_of('fear') // 4)
        
        self.stats.resource_change('fear', amount)
    
    def affect_stress(self, affect:Damage, attacker:BattlePeep):
        
        amount = affect.amount
        
        # When healing stress, 25% of attacker's rec is added
        if affect.is_heal:
            amount += (attacker.value_of('rec') // 4)
        # If taking stress damage, 25% of self tres is used to resist
        else:
            amount -= (self.value_of('tres') // 4)
        
        self.stats.resource_change('tres', amount)
        
    def affect_hp(self, affect:Damage, attacker:BattlePeep):
        '''
        Handles damage dealt to this peep. This includes
        Evading attacks
        
        Returns:
            if evaded
        '''
        I_evaded = False
        
        # Only evade damaging moves
        # in future, casting healing on undead could damage them and thus undead could evade
        if affect.evadable: 
            I_evaded = self.try_to_evade(attacker)
        
        if I_evaded:
            return True # how much evade health was affected, and that no damage was taken
        
        if self.stance() == Peep_State.DEAD:
            # handle revivals
            return
        
        amount = affect.amount
        
        # when bleeding out
        if self.stance() == Peep_State.BLEEDING_OUT: 
            
            past_bleed_out = self.battle_handler.bleed_out
            
            # 1/4 of def comes into play to resisting blood attacks
            if amount < 0:
                amount -= self.value_of("def") / 4
                amount = 0 if amount > 0 else amount # stop blood damage from healing
            
            self.battle_handler.affect_bleed_out(amount)
            '''
            If bleed out hp >= max hp then set current hp equal 
            to overflow from max_hp (minimum 1)
            '''
            if amount > 0 and self.battle_handler.bleed_out >= self.battle_handler.bleed_out_max:
                restored_hp = past_bleed_out + amount - self.battle_handler.bleed_out_max + 1
                self.stats.resource_change('hp', restored_hp)
            
            return # info of how bleed was affected
        
        resisting_stat_amnt = 0
        # get stat to resist against damage
        if not affect.is_heal:
            #amnt_before = amount
            resisting_stat_amnt = self.value_of(affect.resisting_stat)
            
            #check for defense health effect
            #TODO: have peep choose to block
            if self.armor() > 0 and sn(affect.resisting_stat) == sn('def'):
                resisting_stat_amnt = resisting_stat_amnt
            else:
                resisting_stat_amnt /= 4
                
            amount += resisting_stat_amnt
            amount = int(round(amount))
            # don't let resisting damage heal!
            if amount >= 0:
                amount = -1
                
            self.change_defense_health( amount )
            #print(f"| Resisted by {affect.resisting_stat}: {resisting_stat_amnt}! {amnt_before} -> {amount}", end="")
        
        # apply damage   
        depleted = self.stats.resource_change('hp', amount)
        
        # knock out
        if depleted:
            self.battle_handler.start_bleeding_out(self.stats.get_stat_cur('hp').val_active)
            #print(f"\n{self.name} is bleeding out!")
            self.init_growth = 0
            # TODO: affect fear and/or stress. maybe hunger too?
            
    def recover_from_battle_end(self):
        self.stats.resource_set_to_percent('hp', 0.1)
        #TODO: is anything else needed?
        
    def change_evasion_health(self, amount:int):
        self.battle_handler.evasion_health += int(round(amount))
        
        # cap
        self.battle_handler.evasion_health = round(max(0, self.battle_handler.evasion_health))
            
    def change_defense_health(self, amount:int):
        self.battle_handler.defense_health += round(int(round(amount)))
        
        # cap
        self.battle_handler.defense_health = round(max(0, self.battle_handler.defense_health))
 
 
class Peep_State(Enum):
    STANDARD = auto()
    FLYING = auto()
    PRONE = auto()
    HANGING = auto()
    BLEEDING_OUT = auto()
    KNOCKED_DOWN = auto()
    DEAD = auto()
    
    def __str__(self):
        return self.name
        
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
        self.times_made_bleed:int = 0
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
        self.bleed_out = max(1, int(max_hp * (1 - 0.25 * self.times_made_bleed)))
        
        self.times_made_bleed += 1
        
    def handle_bleeding_out(self):
        '''
        Called every battlepeep's turn to check if they are bleeding out
        and dealing with the logic of bleeding out
        
        Returns:
            bool: if peep is dead from bleeding out
        '''
        if self.stance != Peep_State.BLEEDING_OUT:
            return False
        
        self.bleed_out = int(self.bleed_out - self.bleed_out_max * 0.1)
        
        if self.bleed_out <= 0:
            self.die()
            
            return True
        
        return False
    
    def affect_bleed_out(self, amount:int):
        '''        
        when recieving damage: reduce by 80%. 
        received heals are unaffected
        If bleed out hp <= 0 then die
        '''
        # Should peep's stats or magic resist matter?
        amount = amount if amount > 0 else int(amount * 0.2)-1
        
        self.bleed_out += amount
       
        if self.bleed_out <= 0:
            self.bleed_out = 0
            self.die()
        elif self.bleed_out >= self.bleed_out_max:
            self.bleed_out = self.bleed_out_max
            self.stance = Peep_State.STANDARD

    def die(self):
        self.stance = Peep_State.DEAD
        self.times_made_bleed = 0 # TODO: is resetting this the desired behavior?
        #print(f"died!")
        
    def end_battle(self):
        # perhaps stance could be different if char is always flying
        self.stance = Peep_State.STANDARD
        self.bleed_out = 0
        self.bleed_out_max = 0
        self.evasion_health = 0
        self.defense_health = 0
        self.times_made_bleed = 0
        # temp hp can potentially carry over out of battle?
        
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
        
    