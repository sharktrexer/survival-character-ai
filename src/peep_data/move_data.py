'''
Here will contain all move sets for enemies

Generic (most units will have this)

    Basic Attack (Uses STR, + DEX or INT; depending on peep/weapon, attacks DEF)
    Defend (Uses DEF, provides DEF buff)
    Evade (Uses EVA, provides evasion health)
    Sabotage (Attacks gauge stat (not hp))
    Encourage (Heals gauge stat (not hp))
    
    Shove (Change enemies stance to Knocked Down. 
        Requires: 1.3x STR to be more than targets current HP
                  Dex to be greater than targets EVA + Evade Health / 4
    )
    
    These are reserved for when game is ported to an engine
        Pick up & Throw

Enemy Specific

    Offensive
    Defensive
    Heal
    Alert
    
    Add Ons (Choose at least 1 to add to move set):
        Alteration/Status Effect
        Gauge Affect
    
    SIGNATURE
    
    
Peep Specific

    Tanks (Ray, Jimmy, Chris, Jayce) [Def]
        Bodyguard, apply to ally to direct all attacks to themself instead
            -Status Effect, owner of effect is the one who casted this
                On_Action_recieved : take action and set target to SE owner
                
            -BattleAction, when casting, pass self into On_Action_Recieved 
            funcs of Status Effects list on BattlePeep target
            
    DPS (Shown, Jimmy, Adan, Chris) [Str + Dex]
        Smackdown, Deals dex + str damage
        - Only useful on Vulnerable targets (Knocked Down or Bleeding Out)
        - 30% of Bleed Out Armor is ignored (80% -> 50%)
    
    Healers (Cindy, Neo, Jayce, Adan, Rebecca) [Rec]
        Heal, heals rec health of an ally
    
    Cindy
        Sexy Dancing, heal an ally
        - Set self to dance stance
        - Increases heal every turn
        - Interrupted by intimidation
    
    Adan
        Burst Heal I, heal an ally for 25% of their max hp + 50% of Rec. 3 turn cooldown
        Burst Heal II, heal an ally for 50% of their max hp + 25% of Rec. 3 turn cooldown
        
    Rebecca
        Unfortunate Boogie, Attack Stress Gauge of an enemy + Str Debuff + heals allies by 5% of max hp
        - All effects increase every turn
        - Increase is Reset by damage
        - Interrupted by intimidation
        
        Snack, heals self for 10% of max hp
        - 10 charges per battle
        
    Lito
        Succy, Vampirism attack, 50% of damage comes back as
        - AP flexible
        - Only useful on Vulnerable targets (Knocked Down or Bleeding Out)
        - Ignores bleed out armor
    
    Ray
        Grapple, choose target and choose between 2 attacks per turn
        - Set self in Grapple state
        - Actions: Grapple Punch, -30% STR & EVA Debuff for 1 trn
        - Finisher, Deal str damage and force target to Knocked Down
        - Enemy can choose to escape grapple using AP vs STR 
            (more AP required the stronger the grappler is)
        - Enemy Evasion action is 50% less effective
        - If Enemy Evades, damage to Evade HP is dealt to grappler 
        State set to Restricted Moves
        Restricted moves change the move set a peep has
        
    Jayce
        Swig, heals hp and give regen (for self only)
        - Only one charge per battle (one use)
        
    Jimmy
        Bully, Attack Stress & Fear Gauges + 20% of Itmd Physical Dmg + Heals and 20% Def Buff to self
        - Can attack allies
        
    Neo
        Sacrifice, die but help allies :)
        - Set self to Bleeding Out at 50% Blood
        - Heal all allies by 75% and buff all stats by 10% for 2 trn
            
    Sean
        Snipe, Attack with Dex + Str
        - Deals +50% damage once Self has been in the Bleed Out State before in this battle
            - CheckBattleEvent behavior
                pass in an event the behavior will subscribe to
                when event triggered, set bool 'triggered' to True
            - Event Manager will let subscribed behavior know when event is triggered
            
    Chris
        Sentinel, Heals team by 10% of max hp + 50% CRE and gives +20% Def Buff for 2 trns
        - 2 turn cooldown
        - Heals for 50% of max Blood if Ally is Bleeding Out

'''
from battle.battle_action import BattleAction

GENERIC = [
    BattleAction("Attack",[]),
    BattleAction("Defend",[]),
    BattleAction("Evade",[]),
    BattleAction("Shove",[]),
]