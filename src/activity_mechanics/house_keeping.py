from activity_mechanics.activities import Objective

class Clean(Objective):
    def __init__(self, name:str, clean_yield:int, room:str):
        self.name = name
        self.clean_yield = clean_yield
        self.room = room

class Barricade(Objective):
    def __init__(self, name:str, def_yield:int, room:str):
        self.name = name
        self.def_yield = def_yield
        self.room = room

'''
activity list, choose barricade:
    -can the player pass basic activity conditions? not stressed out etc-
    if joining group:
        join it
    if creating new activity progress:
        which barricade to do? only show valid choices. 
            -player meets correct stats, and lodge has the resources-
            can exit to main menu
        create activity progress using barricade objective chosen
            add pip cost based on barricade chosen
            take away resource from lodge based on barricade
        
finishing activity:
    give stat bonuses based on barricade completed
    provide resource to lodge
'''