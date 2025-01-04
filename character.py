class Character:
    
    def __init__(self, name: str, desc: str, stats_dict: dict):
        self.name = name
        self.desc = desc
        self.stats = stats_dict
        
    def __str__(self):
        return self.name + ": " + "\n" + self.desc + "\n" + str(self.stats)