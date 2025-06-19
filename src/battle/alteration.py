class Alteration:

    def __init__(self, name: str, value: float, duration: int, ef_stat: str, ef_type: str):
        
        if value < 0 or value == 1:
            raise Exception("Alteration value must be greater than 0 and cannot be 1")
        
        self.name = name # won't be displayed in game, only used for internal equality checks
        self.value = value
        self.is_buff = value > 1
        self.duration = duration #TODO: will be changed into its own object
        self.duration_left = duration
        self.ef_stat = ef_stat
        self.ef_type = ef_type
        
    def __eq__(self, other):
        if isinstance(other, Alteration):
            return (self.name == other.name or (self.value == other.value 
                    and self.duration == other.duration and self.ef_stat == other.ef_stat 
                    and self.ef_type == other.ef_type))
        return NotImplemented
    
    def tick(self):
        self.duration_left -= 1
        return self.duration_left <= 0
        
    def is_this_more_potent(self, alt):
        if not isinstance(alt, Alteration) or self.is_buff != alt.is_buff:
            return None
        
        if self.is_buff:
            return self.value > alt.value
        else:
            return self.value <= alt.value
        
    def apply(self, alt_list:list):
        '''
        Applies this alteration to the list of alterations, assuming
        the list is sorted by potency then duration, the list only regards one stat,
        and the list is populated with Alterations of the same value type as this one
        (buffs or debuffs)
        '''
        if alt_list == []:
            alt_list.append(self)
            return True
        
        for i, a in enumerate(alt_list):
            
            # This alteration is more potent, insert it in front of this index
            # Stats are recalculated if this is inserted in front of the list
            if self.is_this_more_potent(a):
                alt_list.insert(i, self)
                return i == 0 
            
            # If the potency is the same, perhaps this alteration is a copy or is superior
            if self.value == a.value:
                # refresh duration
                if self.duration == a.duration:
                    a.duration_left = a.duration 
                    return False
                # replace alteration in list as it has more duration
                elif self.duration > a.duration:
                    alt_list[i] = self
                    return False
             
            # This alteration is the least potent, add it to the end
            if not self.is_this_more_potent(a) and i == len(alt_list) - 1:
                alt_list.append(self)
                return False
        
# test alterations, applying to base stat values
#TODO: make into a test file
str_buff = Alteration("Minor Strength", 1.2, 5, "Strength", "base")
str_buff2 = Alteration("Major Strength", 2, 1, "Strength", "base")
str_buff3 = Alteration("Itty Bitty Strength", 1.1, 10, "Strength", "base")
str_debuff = Alteration("Minor Weakness", 0.8, 5, "Strength", "base")
str_debuff2 = Alteration("Itty Bitty Weakness", 0.9, 10, "Strength", "base")