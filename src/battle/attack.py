class Attack():
    '''
    Given a stat to associate with and a percent of the stat to utilize,
    a number can be returned to represent how much an attack will deal damage or heal for
    
    Can affect multiple targets
    
    Can inflict alterations or status effects
    
    Example:
        Attack("Strength", 0.5) would return 50% of the strength stat of the attacker as damage to deal
    '''
    def __init__(self, associated_stat_name:str, 
                 percent_of_stat_2_value:float, 
                 is_aoe:bool = False,
                 is_for_team:bool = False,
                 is_heal:bool = False,
                 inflicting_alterations:list=[],
                 inflicting_status_effects:list=[]):
        
        self.percent = percent_of_stat_2_value
        self.stat = associated_stat_name
        self.is_aoe = is_aoe
        self.is_for_team = is_for_team
        self.is_heal = is_heal
        self.alterations = inflicting_alterations
        self.status_effects = inflicting_status_effects
        self.target_names:list[str] = []
        
    def __str__(self):
        return f"{self.percent} of {self.stat}"
        
    def get_value(self, stat_val):
        return int(stat_val * self.percent)