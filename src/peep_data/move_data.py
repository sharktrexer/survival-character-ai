'''
Here will contain all move sets for all peeps
'''
from battle.battle_action import (BattleAction, Damage, create_dmg_preset, create_specific_phys_dmg, 
                                  DealDamage, AugmentDamage, GainEvasion, Condition, ChangeState)

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
        Condition((lambda me, tar: (
            me.stats.get_stat_active("dex") > 
            tar.stats.get_stat_active("eva") * tar.stats.get_resource_ratio("hp") +
            tar.battle_handler.evasion_health // 4
            )), 
            ABORT=True,
        ),
        ChangeState("Knocked Down"),
        Condition((lambda me, tar: (
            me.str * 1.5 > 
            (tar.stats.get_stat_resource("hp") // 2) +
            tar.stats.get_stat_active("def") * tar.stats.get_resource_ratio("hp")
            )), 
        ),
        DealDamage(create_dmg_preset(0.25, Damage.DamageType.Physical)),
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