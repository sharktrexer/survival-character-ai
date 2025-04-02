class Character:
    
    def __init__(self, name: str, desc: str, stats_dict: dict):
        self.name = name
        self.desc = desc
        self.stat_aps = stats_dict
        self.avg_stat_diffs = dict()
        self.avg_diff = 0
        
    def __str__(self):
        return self.name + ": " + "\n" + self.desc + "\n" + str(self.stat_aps)
    
    ''' Prints the formatted difference between two stats'''
    def str_difference(self, m_stat, l_stat, is_reversed=False, no_name=False, is_simple=False):
        
        # get stat vals
        m_stat_val = self.stat_aps[m_stat]
        l_stat_val = self.stat_aps[l_stat]
        
        # Conditional printing vars
        name = self.name if not no_name else ""
        first_stat = m_stat_val if not is_reversed else l_stat_val
        second_stat = l_stat_val if not is_reversed else m_stat_val
        op = "-" if not is_reversed else "+"
        diff = (first_stat - second_stat if not is_reversed 
                else second_stat + first_stat
                )
        
        # format
        if not is_simple:
            return (
                    m_stat  + " " + op + " " + l_stat + " \t\t" + name + "\t (" 
                    + str(first_stat) + " " + op + " " 
                    + str(second_stat) + ") [" 
                    + str(diff) + "]"
                    )    
        else:
            return (
                    name + "= (" + str(first_stat) + " " + op + " " 
                    + str(second_stat) + ") [" + str(diff) + "]"
                    )   
    
    def get_emotional_stats(self):
        return {stat: self.stat_aps[stat] for stat in 
                ["Fear", "Intimidation", "Charisma", "Stress", "Hunger", "Creativity"]}
        
    def get_physical_stats(self):
        return {stat: self.stat_aps[stat] for stat in 
                ["Strength", "Defense", "Evasion", "Dexterity", "Intellect", "Recovery", "Health", "Energy"]}
        
