from random import randint
from battle.battle_peep import Peep_State
from .battle_action import BattleAction, BattlePeep
from peep_data.move_data import MOVE_SETS

def what_do(myself:BattlePeep, battlers:list[BattlePeep], moves:list[BattleAction]):
    '''
    How are things? do i want to prioritize self, offense, or support?
    ignore dead peeps
    mostly ignore knocked down enemies
    
    if battle is looking fine, randomly choose to help self or offense
    
    if team is looking bad, heal lowest hp ally, or support all if possible
    
    if enemies are looking low, try to finish them off
    
    '''
    
    cleaned_name = myself.name.split()[0]
    avail_moves = MOVE_SETS[cleaned_name]
    
    moves = [m for m in avail_moves if myself.stats.get_stat_resource('ap') >= m.ap]
    
    choices = []
    
    while myself.stats.get_stat_resource('ap') > 0:
        
        # coin flip to save 50% ish of ap for next round
        save_ap = 0
        if myself.stats.get_stat_resource('ap') <= myself.stats.get_stat_active('ap') // 2:
            save_ap = randint (0, 4)
        
        if save_ap > 1:
            break
        
        # if only self moves are left then do them
        for m in moves:
            if m.for_self:
                do_self_move = True
            else :
                do_self_move = False
        
        do_self_move = randint(0,1) or do_self_move
        
        # coin flip to use a selfish move
        if do_self_move:
            self_moves = [move for move in moves if move.for_self]
            random_move = self_moves[randint(0, len(self_moves)-1)]
            
            if random_move.flexible:
                amount_to_spend = randint(1, myself.stats.get_stat_resource('ap'))
                choices.append((random_move, myself, amount_to_spend))
                myself.stats.resource_change('ap', amount_to_spend)
            else:
                choices.append((random_move, myself))
                myself.stats.resource_change('ap', -random_move.ap)
            
            moves = [m for m in avail_moves if myself.stats.get_stat_resource('ap') >= m.ap]
            continue
            
            
        allies = [battler for battler in battlers if battler.team == myself.team]
        enemies = [battler for battler in battlers if battler.team != myself.team]
            
        # only get alive peeps
        allies_v = [ally for ally in allies if ally.battle_handler.stance != Peep_State.DEAD]
        enemies_v = [enemy for enemy in enemies if enemy.battle_handler.stance != Peep_State.DEAD]
        
        # sort peeps by hp
        allies_by_hp = sorted(allies_v, key = lambda peep: peep.stats.get_stat_resource('hp')/peep.stats.get_stat_active('hp'), reverse=True)
        enemies_by_hp = sorted(enemies_v, key = lambda peep: peep.stats.get_stat_resource('hp')/peep.stats.get_stat_active('hp'), reverse=True)
        
        heal_chance = 0.5
        dmg_chance = 0.5
        
        ''' MOVE TYPE CHOICE '''   
        chance_inc = 1 / len(allies_v)
        for a in allies_v:
            if a.stats.get_stat_resource('hp')/a.stats.get_stat_active('hp') <= 0.5:
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
        best_ally_targets = [ally for ally in allies_by_hp if ally.stats.get_stat_resource('hp')/ally.stats.get_stat_active('hp') <= 0.75]
        
        if do_heal:
            random_target = best_ally_targets[randint(0, len(best_ally_targets)-1)]
        else:
            random_target = enemies_by_hp[randint(0, (len(enemies_by_hp)-1)//2)]
            
        heal_moves = [move for move in moves if move.action_type == 'heal']
        dmg_moves = [move for move in moves if move.action_type == 'dmg']
        
        if do_heal:
            if heal_moves == []:
                break
            random_move = heal_moves[randint(0, len(heal_moves)-1)]
        else:
            if dmg_moves == []:
                break
            random_move = dmg_moves[randint(0, len(dmg_moves)-1)]
            
        choices.append((random_move, random_target))
        myself.stats.resource_change('ap', -random_move.ap)
        moves = [m for m in avail_moves if myself.stats.get_stat_resource('ap') >= m.ap]
    
    return choices
