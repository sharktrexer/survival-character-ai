class Plant():
    def __init__(self, name:str, req_seeds:int, ingr_yield:int, days_to_grow:int, req_rec:int):
        self.name = name
        self.req_seeds = req_seeds
        self.ingr_yield = ingr_yield
        self.growth_time = days_to_grow
        self.req_rec = req_rec

'''
Relationship between seeds to yield to time to grow to recovery stat required

'''
        
PLANTS = [
    # base plant
    Plant('Wheat', req_seeds=1, ingr_yield=2, days_to_grow=2, req_rec=0),
    Plant('Rice', req_seeds=2, ingr_yield=6, days_to_grow=6, req_rec=10),
    
    # high seed, high yield
    Plant('Oink Blossom', req_seeds=5, ingr_yield=12, days_to_grow=4, req_rec=50),
    
    # low seed, high yield, high rec
    Plant('Eggplant', req_seeds=1, ingr_yield=8, days_to_grow=2, req_rec=100),
    
    # really good but takes fo eva
    Plant('Fruit Tree', req_seeds=3, ingr_yield=35, days_to_grow=10, req_rec=100),
    
    
]