class Character:
    
    def __init__(self, name: str, desc: str, stats_dict: dict):
        self.name = name
        self.desc = desc
        self.stats = stats_dict
        self.avg_stat_diffs = dict()
        self.avg_diff = 0
        
    def __str__(self):
        return self.name + ": " + "\n" + self.desc + "\n" + str(self.stats)
    
    ''' Prints the formatted difference between two stats'''
    def str_difference(self, m_stat, l_stat, is_reversed=False, no_name=False, is_simple=False):
        
        # get stat vals
        m_stat_val = self.stats[m_stat]
        l_stat_val = self.stats[l_stat]
        
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
            
    def initiative(self):
        return self.stats["Dexterity"] + self.stats["Evasion"]

    def leadership(self):
        return self.stats["Charisma"] + self.stats["Intimidation"] + self.stats["Fear"]

    def acrobatics(self):
        return self.stats["Dexterity"] + self.stats["Strength"]

    def perception(self):
        return self.stats["Intellect"] + self.stats["Evasion"]

    def skirmish(self):
        return self.stats["Strength"] + self.stats["Defense"] + self.stats["Intimidation"]
