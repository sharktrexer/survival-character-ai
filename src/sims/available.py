'''
Gets all created simulator classes in imported modules and instantiates 
them to be accessed by the main loop
'''
import sims.simulator as simulator
import sims.battle_sim as battle

AVAIL_SIMS = []

def get_available_sims():
    subclasses = simulator.Simulator.__subclasses__()
    # Instantiate
    for cls in subclasses:
        sim = cls()
        AVAIL_SIMS.append((sim.name, sim))
        
    #print(f"Instantiated {len(AVAIL_SIMS)} subclasses.")

