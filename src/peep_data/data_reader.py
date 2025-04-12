import pandas as pd
import os



data = pd.read_csv(os.getcwd() + "//src//peep_data//char_data.csv")
print(data)