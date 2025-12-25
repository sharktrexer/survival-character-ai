class Barricade():
    def __init__(self, name, req_mats:int, def_yield:int):
        self.name = name
        self.req_mat = req_mats
        self.def_yield = def_yield
        
BARRICADES = [
    Barricade("Cloth", req_mats=1, def_yield=1),
    Barricade("Wood", 3, 5),
    Barricade("Sheet Metal", 8, 18),
    Barricade("Pure Metal", 12, 30),
]