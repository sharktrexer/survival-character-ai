class Calcs():
    
    @staticmethod
    def clamp_int(val:int, min_v:int, max_v:int):
        return int(Calcs.clamp(val, min_v, max_v))
    
    @staticmethod
    def clamp(val, min_v, max_v):
        return max(min_v, min(val, max_v))