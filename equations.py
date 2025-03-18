from character import Character

def get_cur_init(peep: Character, anchor):
    rounds_passed = 0 # get from "battle manager"
    init_growth = ((peep.initiative() - anchor)*rounds_passed) # stored in Character
    gain_bonus = peep.initiative() + init_growth - anchor >= 2(anchor)
    # reset round counter
    if gain_bonus:
        rounds_passed = 0
    return gain_bonus