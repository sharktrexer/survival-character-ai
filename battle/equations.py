from peep.character import Character

def do_gain_bonus_AP_from_init(peep: Character, anchor_init):
    rounds_passed = 0 # get from Character
    init_growth = ((peep.initiative() - anchor_init)*rounds_passed) # stored in Character
    gain_bonus = peep.initiative() + init_growth - anchor_init >= 2(anchor_init)
    # reset round counter
    if gain_bonus:
        rounds_passed = 0
    return gain_bonus