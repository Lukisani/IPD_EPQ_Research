import os
import pandas as pd
import csv

'''
Example of file path:
'./figures/tournament_standings.pdf'
'./game_stats/original_data/match_results.csv'
'''

def save_csv_file(dataframe, folder_path, filename):
    file_path = os.path.join(folder_path, filename)

    # Check if file exists before saving
    if not os.path.exists(file_path):
        dataframe.to_csv(file_path, index=False)
        print(f"{filename} saved successfully.")
    else:
        print(f"{filename} already exists. Not saving.")


def save_pdf_file(fig, folder_path, filename):
    file_path = os.path.join(folder_path, filename)

    # Check if file exists before saving
    if not os.path.exists(file_path):
        fig.savefig(file_path)
        print(f"{filename} saved successfully.")
    else:
        print(f"{filename} already exists. Not saving.")

def create_folder(new_folder_path):
    # Check if the folder already exists
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Folder created successfully at: {new_folder_path}")
    else:
        print(f"Folder already exists at: {new_folder_path}... Not saving")

def create_meta_file(folder_path, filename, **kwargs):
    file_path = os.path.join(folder_path, filename)

    # Check if file exists before saving
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            for key, value in kwargs.items():
                file.write(f'{key}: {value}\n')
        print(f"{filename} saved successfully.")
    else:
        print(f"{filename} already exists. Not saving.")

    

def get_direc():
    return {
         'basic_tournaments': './game_stats/basic_tournaments',
         'fig_dir': './figures',
         'noisy_tournaments' : './game_stats/noisy_tournaments',
         'original_data' : './game_stats/original_data'
         }

class ObjectView(object):
    def __init__(self, d): self.__dict__ = d

# direc = ObjectView(get_direc()) <-- function needed to call args
