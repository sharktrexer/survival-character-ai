from battle.stats import sn, convert_whole_number_to_multiplier, reduce_decreasing_modifier, reduce_increasing_modifier
from battle.battle_peep import BattlePeep
from abc import ABC, abstractmethod

class MultChange:
    '''
    Simple class to represent a multiplier stat change. 
    Also can be used for integer changes but requires is_integer=True
    '''
    def __init__(self, stat_name:str, mult, is_integer=False):
        self.name = sn(stat_name)
        self.mult = mult
        self.is_integer = is_integer
        
class MultManipulator(ABC):        

    @abstractmethod
    def get_mult_changes(self, target:BattlePeep) -> list[MultChange]:
        raise NotImplementedError("Method was not implemented despite inheriting from MultManipulator")
    
    #create simple function to take list of changes to stats, mults or whole numbers
    
    def calc_mult_with_peep(self, target:BattlePeep, mults:list[MultChange]):
        '''
        Moify values of mult changes based on game rules
        '''
        for m in mults:
            
            associated_stat = target.stats.get_stat_cur(m.name)
            
            # convert any integer mults to float
            if m.is_integer:
                m.mult = convert_whole_number_to_multiplier(m.mult)
                m.is_integer = False
            
            # make sure negative mults are adjusted by positive aptitude
            if m.mult < 0 and associated_stat.aptitude > 0:
                m.mult = reduce_decreasing_modifier(associated_stat.aptitude, m.mult)
            # and positive mults are adjusted by negative aptitude
            elif m.mult > 0 and associated_stat.aptitude < 0:
                m.mult = reduce_increasing_modifier(associated_stat.aptitude, m.mult)
            
            # apply multiplier, TODO: perhaps a different class handles this?
            target.stats.mult_changes[m.name].mult *= m.mult
            pass
        
        
        
        