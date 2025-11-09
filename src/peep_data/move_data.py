'''
Here will contain all move sets for all peeps
'''
from battle.battle_action import (BattleAction, Damage, create_dmg_preset, create_specific_phys_dmg, 
                                  DealDamage, AugmentDamage, GainEvasion)

UNIVERSAL_MOVES = [

    BattleAction("Block", -1, [
        # Give defense health
        ]),

    BattleAction("Evade", -1, [
        # give evasion health
            GainEvasion(0.3, for_self=True),
        ]),
    BattleAction("Shove", 5, [
        # set target to knocked down if conditions are met
        ]),
]

HUMAN_MOVES = [
    BattleAction("Punch", 3, [
                    AugmentDamage(create_specific_phys_dmg(0.1, 'dex')),
                    DealDamage(create_dmg_preset(0.2, Damage.DamageType.Physical))
                    ]),
    BattleAction("Kick", 5, [
                    AugmentDamage(create_specific_phys_dmg(0.15, 'eva')),
                    DealDamage(create_dmg_preset(0.3, Damage.DamageType.Physical))
                    ]),
]