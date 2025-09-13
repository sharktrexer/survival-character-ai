''' Character used for data analysis '''
class Character:
    
    def __init__(self, name: str, title: str, desc: str, stats_dict: dict):
        self.name = name
        self.title = title
        self.desc = desc
        self.stat_apts = stats_dict
        self.avg_stat_diffs = dict()
        self.avg_diff = 0
        
    def __str__(self):
        #stringify apt dict
        stringified_apt_dict = ""
        for name, apt in self.stat_apts.items():
            # format non negatives to take same space as negatives
            if apt >= 0:
                apt = " " + str(apt)
                
            stringified_apt_dict += f"{name:<13}= {apt:<3}\n"
        
        return (self.name + ", the " + self.title + "\nStat Details:\n"+ f"{'Name':<12} | {'Value':<3}" 
                + "\n" + stringified_apt_dict)
    
    ''' Prints the formatted difference between two stats'''
    def str_difference(self, m_stat, l_stat, is_reversed=False, no_name=False, is_simple=False):
        
        # get stat vals
        m_stat_val = self.stat_apts[m_stat]
        l_stat_val = self.stat_apts[l_stat]
        
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
        return {stat: self.stat_apts[stat] for stat in 
                ["fear", "intimidation", "charisma", "stress", "hunger", "creativity"]}
        
    def get_physical_stats(self):
        return {stat: self.stat_apts[stat] for stat in 
                ["strength", "defense", "evasion", "dexterity", "intelligence", "recovery", "health", "energy"]}
        
