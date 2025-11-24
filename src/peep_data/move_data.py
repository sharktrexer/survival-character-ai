'''
Here will contain all move sets for all peeps
'''
from battle.alteration import AlterationFactory
from battle.battle_action import (BattleAction, Damage, Peep_State, TargetTypes, 
                                  create_dmg_preset, create_specific_phys_dmg, 
                                  DealDamage, AugmentDamage, GainEvasionHealth, Condition, ChangeState,
                                  ReduceEvasionHealth, GainDefenseHealth, ApplyAlteration,
                                  ReverseCondition, YesCondition, ABORT, AttackEvasion, UNEVADABLE, DMG_MULT)

TEST_MOVES = [
    BattleAction("Attack", 6, [
        DealDamage(create_dmg_preset(0.6, Damage.DamageType.Physical))
        ],
                 valid_targets=[TargetTypes.ENEMY],),
    
    BattleAction("Magic", 6, [
        DealDamage(create_dmg_preset(0.6, Damage.DamageType.Magical))
        ],
                 valid_targets=[TargetTypes.ENEMY],),
]

UNIVERSAL_MOVES = [

    
    
    BattleAction("Heal", 8, [
        UNEVADABLE(),
        DealDamage(create_dmg_preset(0.8, Damage.DamageType.Healing))
        ],
                 valid_targets=[TargetTypes.ALLY, TargetTypes.SELF],
                 ),
    
    BattleAction("Evade", 1, [
        # give evasion health
        GainEvasionHealth(0.3, for_self=True),
        ],
        valid_targets=[TargetTypes.SELF],
        ap_flexible=True),
    
    BattleAction("Block", 1, [
        # Give defense health
        GainDefenseHealth(0.3, for_self=True),
        ],
        valid_targets=[TargetTypes.SELF],
        ap_flexible=True),
    
    BattleAction('Bulwark', 5, [
        # give lots of defense health, but requires more investment
        GainDefenseHealth(1.85, for_self=True),
        ],
        valid_targets=[TargetTypes.SELF],
        ap_flexible=True),
    
    BattleAction('Harden', 3, [
        # provides defense buff
        ApplyAlteration(
            AlterationFactory.create_alteration
            (
                "def", 1.5, 1 ), 
            for_self=True),
        ],
        valid_targets=[TargetTypes.SELF],
        ),
    
    BattleAction("Shove", 5, [
        UNEVADABLE(),
        Condition((lambda me, tar: (
            me.value_of("dex") > 
            tar.value_of("eva") * tar.stats.get_resource_ratio("hp") +
            tar.battle_handler.evasion_health // 4
            )), 
        ),
        ReduceEvasionHealth(0.25),
        ReverseCondition(),
        AttackEvasion(), 
        ABORT(),
        Condition((lambda me, tar: (
            me.value_of("str") * 1.5 > 
            (tar.points_of("hp") // 2) +
            tar.value_of("def") * tar.stats.get_resource_ratio("hp")
            )), 
        ),
        ChangeState(Peep_State.KNOCKED_DOWN),
        DealDamage(create_dmg_preset(0.25, Damage.DamageType.Physical)),
        ],
        valid_targets=[TargetTypes.ENEMY],),
]

''' Enemy moves '''
RAT_MOVES = [
    BattleAction("Bite", 3, [
        DealDamage(create_dmg_preset(0.95, Damage.DamageType.Physical))
    ],
    valid_targets=[TargetTypes.ENEMY],
    ),
    
    BattleAction("Scurry", 4, [
        ApplyAlteration(
        AlterationFactory.create_alteration(
            "eva", 1.5, 2), 
        for_self=True),
        GainEvasionHealth(0.6, for_self=True)
    ],
    valid_targets=[TargetTypes.SELF],
    ),
    
    BattleAction("Cheese Bounty", 6, [
        DealDamage(create_dmg_preset(0.4, Damage.DamageType.Healing), for_self=True),
        DealDamage(create_dmg_preset(0.8, Damage.DamageType.Healing))
        
    ],
                 valid_targets=[TargetTypes.ALLY],
                 ),
    
    BattleAction('Caca Time', 4, [
        # attack stress gauge
        ApplyAlteration(
        AlterationFactory.create_alteration(
            "def", 1.5, 2), 
        for_self=True),
    ],
                 valid_targets=[TargetTypes.SELF],
                 ),
    
    # BattleAction("Mighty Squeak", 8, [
    #     # Summon rat if rat hole present
    # ]),
    
    # BattleAction("RATATOUILLE", 8, [
    #     # Give allies regen. +30% for 2 trns
    #     # heal all allies stress health
    # ],
    #              valid_targets=[TargetTypes.ALLY],)
    ]


# current economy: 
# for every 2 ap, 0.3 of a stat can be used as dmg
# for every 1 ap, 0.3 of a stat can be used defensively
# for every 1 ap, 0.2 of a stat is used for healing
''' PEOPLE MOVES '''
HUMAN_MOVES = [
    BattleAction("Punch", 2, [
        AugmentDamage(create_specific_phys_dmg(0.1, 'dex')),
        DealDamage(create_dmg_preset(0.2, Damage.DamageType.Physical))
        ],
                 valid_targets=[TargetTypes.ENEMY],
                 ),
    BattleAction("Kick", 3, [
        AugmentDamage(create_specific_phys_dmg(0.15, 'eva')),
        DealDamage(create_dmg_preset(0.3, Damage.DamageType.Physical))
        ],
                 valid_targets=[TargetTypes.ENEMY],
                 ),
]

SEAN_MOVES = [
        BattleAction("Snipe", 6, [
            Condition((lambda me, tar: (
                me.battle_handler.times_made_bleed > 0
                ))
            ),
            DMG_MULT(1.5),
            YesCondition(),
            AugmentDamage(create_specific_phys_dmg(0.4, 'dex')),
            DealDamage(create_dmg_preset(0.3, Damage.DamageType.Physical))
            ],
                     valid_targets=[TargetTypes.ENEMY],),
]

MOVE_SETS = {
    'Adan': HUMAN_MOVES + UNIVERSAL_MOVES,
    'Chris': HUMAN_MOVES + UNIVERSAL_MOVES,
    'Cindy': HUMAN_MOVES + UNIVERSAL_MOVES,
    'Ray': HUMAN_MOVES + UNIVERSAL_MOVES,
    'Jimmy': HUMAN_MOVES + UNIVERSAL_MOVES,
    'Neo': HUMAN_MOVES + UNIVERSAL_MOVES,
    'Lito': HUMAN_MOVES + UNIVERSAL_MOVES,
    'Jayce': HUMAN_MOVES + UNIVERSAL_MOVES,
    'Rebecca': HUMAN_MOVES + UNIVERSAL_MOVES,
    'Sean': HUMAN_MOVES + UNIVERSAL_MOVES + SEAN_MOVES,
    'Rat': UNIVERSAL_MOVES + RAT_MOVES,
    'Heavy_Slime': UNIVERSAL_MOVES,
    'Ent': UNIVERSAL_MOVES,
    'Double_Rat': UNIVERSAL_MOVES,
}