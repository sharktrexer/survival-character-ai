from collections import namedtuple
from enum import Enum, auto
from random import randint
from battle.battle_peep import Peep_State
from battle.battle_manager import BattleManager, MoveChoice
from .battle_action import BattleAction, BattlePeep
from peep_data.move_data import MOVE_SETS

'''
TARGETING
Before each action, a prime ally and enemy target are chosen
-Basic priority:
    Enemies that are weak to your stats 
        (High dex targets High Eva, High STR targets low DEF)
    Allies that compensate for your weaknesses
        (Low eva/def/rec targets high eva/def/rec)
-Then the targets that meet the personality's stat criteria

-Then custom criteria
    Knocked down targets
    Targets with x status effect
    Targets with x% of resource
    
After simulating a 1/3 move per action on a target, 
if overall points are low choose a new target
and temporarily decrease target's targetability (they will not be targeted as much)
'''


'''
QUIRK
-Empathy: Ratio of Selfish (Target self) to Selfless (Target allies)
    selfishness increase as critical health approaches
-Stacking: how often they like to repeat effects
-Focus: how often they stay focused on one target vs changing it up
'''

'''
GOAL
-Offensive: -Health, -Dodge, -Armor
-Heal: +Health
Above bases points on percent of dmg healed/dealt vs max health
-Defensive: +Dodge, +Armor
    more points given when unprotected or without much protection
-Alteration: +Buff, +Debuff
    recieve points based on power of Alteration
    if target would be more affected by this Alteration
    if it would refresh an almost expiring Alteration
    

'''

'''
> Offensive (Dealing damage to enemies)
> Defensive (Gaining Defense or Evasion Health)
> Heal (Restoring health back)
> Status effect (Applying a status effect)
    Defensive (reduce damage taken or prevent negative effects)
    Offensive (deal damage or increase vulnerability)
    Redirection (Force change the target of a recieved or outgoing action)
        Pacify (Force target to target another, offensive moves are worse)
        Taunt (Force target to target you, non-offensive moves are worse)
        Counter
        Bodyguard (Let self take damage for ally)
        Hostage (Force a target to take damage for self)
    Limitation (Preventing certain actions being cast)
    Team Switching (Set a target to work for you or against others)
    Trapping (Force attacker to be hurt if they try to attack)
> Alteration (Applying an alteration)
    Buff
    Debuff
> Gauge Effect (Affecting Fear, Stress, Energy, Hunger resources)
    Damage
    Heal
> Socialize (Encourage allies to do something)
    Suggest (Offer for the ally to combo with you)
    Command (Force a target to use an action)
        (Works when target has less ITMD/CHA Aptitude and high FEAR)
        (Works best on targets afflicted with negative psychic effects)
    Bargain (Offer a target something to get them to do something else)
        (Can be used regardless of stat differences, though CHA helps)
        (Offers could be Healing Gauges, Self locking out an action, etc)
    Alert (Attract allies from other rooms or spawning objects)
> Summon (Create new allies out of thin air)
> Sacrificial (Hurting self for some benefit)
> Stance Change (Change stance of something)
    Dancing
    Prone
    Flying
    Grappling
'''

class BattleAffects(Enum):
    HEALTH = auto()
    EVADE = auto()
    ARMOR = auto()

Desire = namedtuple('affect', 'sign')
    
class Goal:
    def __init__(self, name:str, desires:list[BattleAffects], priority:int):
        self.name = name
        self.desires = desires
        self.priority = priority



class BattleAI:
    
    def __init__(self, myself:BattlePeep):
        self.myself = myself
        self.moves:list[BattleAction] = MOVE_SETS[self.myself.key_name]
        self.choices:list[MoveChoice] = []
        self.my_ap = self.myself.points_of('ap')
        self.can_still_cast = True

    def what_do(self, battlers:list[BattlePeep]):
        '''
        How are things? do i want to prioritize self, offense, or support?
        ignore dead peeps
        mostly ignore knocked down enemies
        
        if battle is looking fine, randomly choose to help self or offense
        
        if team is looking bad, heal lowest hp ally, or support all if possible
        
        if enemies are looking low, try to finish them off
        
        '''            
        
        used_flex_move = False # temporarily just use on for self move at a time
        
        # choose moves while energy remains, there are moves left, 
        # and less than 3 moves have been chosen
        while self.can_still_cast:
            
            # coin flip to save 50% ish of ap for next round
            save_ap = 0
            if self.my_ap <= self.myself.value_of('ap') // 2:
                save_ap = randint (0, 6)
            
            if save_ap > 1:
                break
            
            # if only self moves are left then do them
            selfish_moves = [move for move in self.moves if move.for_self_only]
            
            do_self_move = randint(0,1) and selfish_moves != []
            
            # coin flip to use a selfish move
            # depending on personality selfishness, will choose for self only moves
            # including moves that can be used on allies, but only targeting self
            # based on stats, choose to evade (eva) or block (def)
            if do_self_move:
                random_move = selfish_moves[randint(0, len(selfish_moves)-1)]
                
                if random_move.flexible:
                    if used_flex_move:
                        continue
                    # take into account flexible moves that require more ap per cast
                    # sees how many times, using move ap cost, can go ito myself ap resource
                    # randomly chooses how many times, minimum 1
                    num_of_uses = self.my_ap // random_move.ap
                    # then spend that many times of move ap
                    amount_to_spend = randint(1, num_of_uses) * random_move.ap
                    move = MoveChoice(random_move, self.myself, amount_to_spend)
            
                    self.update_peep_move_state(move)
                    #used_flex_move = True
                else:
                    move = MoveChoice(random_move, self.myself, random_move.ap)
            
                    self.update_peep_move_state(move)
                
                continue
                
                
            allies = [battler for battler in battlers if battler.team == self.myself.team]
            enemies = [battler for battler in battlers if battler.team != self.myself.team]
                
            # only get alive peeps
            allies_v = [ally for ally in allies if ally.stance() != Peep_State.DEAD]
            enemies_v = [enemy for enemy in enemies if enemy.stance() != Peep_State.DEAD]
            
            # sort peeps by hp
            allies_by_hp = sorted(allies_v, key = lambda peep: peep.points_of('hp')/peep.value_of('hp'), reverse=True)
            enemies_by_hp = sorted(enemies_v, key = lambda peep: peep.points_of('hp')/peep.value_of('hp'), reverse=True)
            
            heal_chance = 0.5
            dmg_chance = 0.5
            
            ''' MOVE TYPE CHOICE '''   
            chance_inc = 1 / len(allies_v)
            for a in allies_v:
                if a.points_of('hp')/a.value_of('hp') <= 0.5:
                    heal_chance += chance_inc 
                    dmg_chance -= chance_inc
                    # increase chance to pick a support move
                    # add targets to potential pool if they meet hp threshold
            
            # if not enough allies have taken dmg, dont heal        
            if heal_chance < 0.61:
                heal_chance = 0
                dmg_chance = 1
            
            ''' TARGET CHOICE '''
            
            do_heal = False
            
            heal_chance *= 100
            dmg_chance *= 100
            
            # choose between heal or dmg based on chances
            move_type_to_use = randint(1,100)
            
            if move_type_to_use <= heal_chance:
                do_heal = True
            
            # only get allies that have less than 75% hp
            best_ally_targets = [ally for ally in allies_by_hp if ally.points_of('hp')/ally.value_of('hp') <= 0.75]
            
            if do_heal:
                random_target = best_ally_targets[randint(0, len(best_ally_targets)-1)]
            else:
                random_target = enemies_by_hp[randint(0, (len(enemies_by_hp)-1)//2)]
                
            heal_moves = [move for move in self.moves if move.action_type == 'heal']
            dmg_moves = [move for move in self.moves if move.action_type == 'dmg']
            
            if do_heal:
                if heal_moves == []:
                    break
                random_move = heal_moves[randint(0, len(heal_moves)-1)]
            else:
                if dmg_moves == []:
                    break
                random_move = dmg_moves[randint(0, len(dmg_moves)-1)]
            
            move = MoveChoice(random_move, random_target, random_move.ap)
            
            self.update_peep_move_state(move)
        
    
    def update_peep_move_state(self, move:MoveChoice):
        self.choices.append(move)
        self.my_ap -= move.ap_spent
        self.moves = [m for m in self.moves if self.my_ap >= m.ap]
        self.can_still_cast = self.my_ap > 0 and len(self.moves) > 0 and len(self.choices) < 3
        
        
def simulate(ai:BattleAI, battle:BattleManager):
    # get ai state and battle data from each move
    # calculate points based on goals
    # call simulate again on moves where points >= median of points from all move
    # return all simulates += moves for Ai to execute
    pass