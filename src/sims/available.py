'''
Gets all created simulator classes in the simulator module and instantiates 
them to be accessed by the main loop
'''
import sims.simulator as simulator
import inspect

AVAIL_SIMS = []

def get_available_sims():
    '''
    Fetches all non-abstract Simulator's in the simulator module and instantiates
    them for use in the main loop. They are added to AVAIL_SIMS as a tuple of
    (instance name, instance)
    '''
    concrete_classes = [
        sims for name, sims in inspect.getmembers(simulator)
        if inspect.isclass(sims) and not inspect.isabstract(sims) 
        and issubclass(sims, simulator.Simulator) 
    ]

    # Instantiate the filtered classes with their name as the key
    for sims in concrete_classes:
        sim = sims()
        AVAIL_SIMS.append((sim.name, sim))
