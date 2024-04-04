import numpy as np
import pandas as pd
import json

data = pd.read_csv('anime_genre.csv')

copy_data = data.copy()


def genre():
    updated_dict_list = []

    for index, row in copy_data.iterrows():
        row_dict = {
            'URL': row['Image URL'],
            'Name': row['Name'],
            'Genre': row['Genre'],
            'Type': row['Type'],
            'Score': str(row['Score']),
            'Episodes': str(row['Episodes'])
        }
        updated_dict_list.append(row_dict)

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data  # Yaha return kar rahe hain instead of print