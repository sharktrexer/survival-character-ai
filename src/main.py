from peep_data.char_data import get_peeps_as_simple
from sims.available import AVAIL_SIMS, get_available_sims

# read character data and populate SIMPLE_PEOPLE
get_peeps_as_simple()
# obtain all available sims
get_available_sims()
# initialize db after char data is loaded
import peep_data.combo_db as c
c.initialize_combos_db()

def main():
        
    print("\n\nWelcome to the peep simulator!\n" +
          "Here you can choose different simulations to run," 
          "from displaying data, or controlling a battle.")
    
    while True:
        valid = False
        choice = ""
        
        while not valid:
            print("\nPick a simulator from the list below:")
            for i, s in enumerate(AVAIL_SIMS):
                print(s[0], f"[{i+1}]")
                
            choice = input((f"Pick a number from  1-{len(AVAIL_SIMS)} \n")).lower()
            try:
                choice = int(choice) - 1
            except:
                continue
            valid = choice >= 0 and choice < len(AVAIL_SIMS)
            
        AVAIL_SIMS[choice][1].simulate()


if __name__ == "__main__": main()