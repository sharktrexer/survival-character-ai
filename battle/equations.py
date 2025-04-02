from battle_peep import BattlePeep

def do_gain_bonus_AP_from_init(peep: BattlePeep, anchor_init):

    peep.init_growth = (
        (peep.initiative() - anchor_init) * peep.init_rounds_passed ) 
    gain_bonus = peep.initiative() + peep.init_growth - anchor_init >= 2(anchor_init)
    # reset round counter
    if gain_bonus:
        peep.energy_bonus()
        
    return gain_bonus