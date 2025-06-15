class Alteration:

    def __init__(self, name: str, value: float, duration: int, ef_stat: str, ef_type: str):
        
        if value < 0 or value == 1:
            raise Exception("Alteration value must be greater than 0 and cannot be 1")
        
        self.name = name
        self.value = value
        self.duration = duration
        self.ef_stat = ef_stat
        self.ef_type = ef_type
        
# test alterations, applying to base stat values
str_buff = Alteration("Minor Strength", 1.2, 5, "Strength", "base")
str_buff2 = Alteration("Major Strength", 2, 1, "Strength", "base")
str_buff3 = Alteration("Itty Bitty Strength", 1.1, 10, "Strength", "base")
str_debuff = Alteration("Minor Weakness", 0.8, 5, "Strength", "base")
str_debuff2 = Alteration("Itty Bitty Weakness", 0.9, 10, "Strength", "base")