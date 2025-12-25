class Meal():
    def __init__(self, name:str, req_ingr:int, req_cre:int, hun_rest:int, serves:int=1):
        self.name = name
        self.req_ingr = req_ingr
        self.req_cre = req_cre
        self.hun_rest = hun_rest
        self.serves = serves

'''
Relationship between ingredients to yield to required creativity to hunger restored to servings

'''
        
MEALS = [
    # base food
    Meal('Toast', req_ingr=1, req_cre=0, hun_rest=10),
    Meal('Fried Egg', 1, 10, 15),
    # minor cre needed
    Meal('Pancake', 3, 15, 20),
    Meal('Sandwich', 2, 30, 25),
    # low cre bu high ingredient:
    Meal('Trail Mix', 5, 20, 15, serves=4),
    
    # high cre low ingredients
    Meal('Omlette', 2, 80, 40),
    
    # high cre and ingredients needed
    Meal('Pot Roast', 10, 100, 30, serves=10),
    

    
]