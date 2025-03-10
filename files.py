import os
import pandas as pd
import csv

'''
Example of file path:
'./figures/tournament_standings.pdf'

'''

def save_file(dataframe, folder_path, filename):
    file_path = os.path.join(folder_path, filename)

    # Check if file exists before saving
    if not os.path.exists(file_path):
        dataframe.to_csv(file_path, index=False)
        print(f"{filename} saved successfully.")
    else:
        print(f"{filename} already exists. Not saving.")
