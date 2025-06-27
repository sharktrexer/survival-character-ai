from peep_data.char_data import peep_fetch
from sims.available import AVAIL_SIMS, get_available_sims

# read character data and populate SIMPLE_PEOPLE
peep_fetch()
# obtain all available sims
get_available_sims()

def main():
        
    """
    Displays a welcome message for the peep simulator and prompts the user to select a 
    simulation to from AVAIL_SIMS where the user can choose one by inputting a number. 
    Validates user input to ensure a correct choice is made, then executes the selected simulation.
    """
    print("\n\nWelcome to the peep simulator!\n" +
          "Here you can choose different simiulations to run," 
          "from displaying data, or controlling a battle.\n")
    
    
    while True:
        valid = False
        choice = ""
        
        while not valid:
            print("Pick a simulator from the list below:")
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