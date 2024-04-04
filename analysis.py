import json
import numpy as np
import pandas as pd
from datetime import datetime

anime = pd.read_csv('anime-dataset-2023.csv')

def to_float(value):
    if value == 'UNKNOWN':
        return float(-1.0)
    else:
        return float(value)


def to_rank(value):
    if (value == 'UNKNOWN') | (value == '0.0'):
        return float(20105.0)
    else:
        return float(value)


anime['Rank'] = anime['Rank'].apply(to_rank)
anime['Scored By'] = anime['Scored By'].apply(to_float)
anime['Popularity'] = pd.to_numeric(anime['Popularity'])
anime['Favorites'] = pd.to_numeric(anime['Favorites'])
anime['Members'] = pd.to_numeric(anime['Members'])

def process_aired_dates(aired):
    # Split the 'Aired' column into start and end dates
    if 'to' in aired:
        start_date_str, end_date_str = aired.split(' to ')
    else:
        start_date_str = aired
        end_date_str = None

    # Convert the date strings to datetime objects
    try:
        start_date = datetime.strptime(start_date_str.strip(), '%b %d, %Y') if start_date_str else None
    except ValueError:
        start_date = None

    try:
        end_date = datetime.strptime(end_date_str.strip(), '%b %d, %Y') if end_date_str else None
    except ValueError:
        end_date = None

    return start_date, end_date

# Apply the function to the 'Aired' column
anime['Start Date'], anime['End Date'] = zip(*anime['Aired'].apply(process_aired_dates))

anime_copy = anime.copy()


def top_1000():
    # Yaha pe, top 1000 rows ko select kar rahe hain
    ranking_data = anime_copy[
        ['Image URL', 'Name', 'Start Date', 'End Date', 'Genres', 'Score', 'Synopsis', 'Rating', 'Scored By',
         'Rank']].sort_values('Rank').head(1000)  # top 1000 rows

    updated_dict_list = []

    for index, row in ranking_data.iterrows():
        start_year = str(row['Start Date']).split('-')[0] if pd.notna(row['Start Date']) else None
        end_year = str(row['End Date']).split('-')[0] if pd.notna(row['End Date']) else None

        row_dict = {
            'URL': row['Image URL'],
            'Rank': str(row['Rank']),
            'Name': row['Name'],
            'Start year': str(start_year),
            'End year': str(end_year),
            'Genre': row['Genres'],
            'Score': str(row['Score']),
            'Description': row['Synopsis'],
            'Rating': row['Rating'],
            'Votes': str(row['Scored By'])
        }
        updated_dict_list.append(row_dict)

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data  # Yaha return kar rahe hain instead of print

def all_Anime():
    # Yaha pe, top 1000 rows ko select kar rahe hain
    all_anime = anime_copy[['Image URL','Name','Type','Start Date']]

    updated_dict_list = []

    for index, row in all_anime.iterrows():
        start_year = str(row['Start Date']).split('-')[0] if pd.notna(row['Start Date']) else None

        row_dict = {
            'URL': row['Image URL'],
            'Name': row['Name'],
            'Type': row['Type'],
            'Start year': str(start_year)
        }
        updated_dict_list.append(row_dict)

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data  # Yaha return kar rahe hain instead of print