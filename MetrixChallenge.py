# importing libraries
import pandas as pd
import re
import json
from collections import Counter

data = pd.read_csv('anime-dataset-2023.csv')

# Preprocessing data
# Function to convert duration strings to minutes
def duration_to_minutes(duration_str):
    if pd.isnull(duration_str):
        return None
    hours = minutes = 0
    hour_search = re.search(r'(\d+)\s*hr', duration_str)
    minute_search = re.search(r'(\d+)\s*min', duration_str)
    if hour_search:
        hours = int(hour_search.group(1))
    if minute_search:
        minutes = int(minute_search.group(1))
    total_minutes = hours * 60 + minutes
    return total_minutes if total_minutes > 0 else None

# Apply the conversion to the Duration column
data['Duration'] = data['Duration'].apply(duration_to_minutes)

def rate_change(s):
    ns = ''
    if s == 'R - 17+ (violence & profanity)':
        ns = 'R - 17'
        return ns
    elif s == 'PG - 13 - Teens 13 or older':
        ns = 'PG - 13'
        return ns
    elif s == 'PG - Children':
        ns = 'PG'
        return ns
    elif s == 'R+ - Mild Nudity':
        ns = 'R'
        return ns
    elif s == 'G - All Ages':
        ns = 'G'
        return ns
    elif s == 'Rx - Hentai':
        ns = 'Rx'
        return ns
    else:
        ns = 'U'
        return ns

data['Rating'] = data['Rating'].apply(rate_change)

# Convert columns to the appropriate numeric types, handling non-numeric values and missing data
data['Score'] = pd.to_numeric(data['Score'], errors='coerce')
data['Episodes'] = pd.to_numeric(data['Episodes'], errors='coerce')
data['Rank'] = pd.to_numeric(data['Rank'], errors='coerce')
data['Scored By'] = pd.to_numeric(data['Scored By'], errors='coerce')

# 1. Total number of anime in the dataset.
def total_anime():
    updated_dict_list = []

    data_dict = {
        'Total Data': str(data.shape[0])
    }
    updated_dict_list.append(data_dict)

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data


def score_data():
    updated_dict_list = []

    data_dict = {
        'Min Score': str(data['Score'].min()),
        'Max Score': str(data['Score'].max()),
        'Avg Score': str(data['Score'].mean())
    }
    updated_dict_list.append(data_dict)

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data


def genre_count():
    # Split the genres for each anime and flatten the list
    all_genres = data['Genres'].str.split(', ').sum()

    # Count the occurrences of each genre
    genre_counts = Counter(all_genres)

    # Identify the most common genre and its count
    genre_counts_dict = dict(genre_counts)

    updated_dict_list = []
    updated_dict_list.append(genre_counts_dict)

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data


def total_eps_basedon_type():
    updated_dict_list = []

    data_dict = data.groupby('Type')['Episodes'].sum().to_dict()
    updated_dict_list.append(data_dict)

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data


def avg_type():
    updated_dict_list = []

    data_dict = {
        'Average Favorites': data['Favorites'].mean()
    }
    updated_dict_list.append(data_dict)

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data


def count_anime_type():
    updated_dict_list = []

    data_dict = data.groupby('Type')['Type'].count().to_dict()
    updated_dict_list.append(data_dict)

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data


def anime_by_rating(rating):
    anime_data = data[data['Rating'] == rating]

    updated_dict_list = []

    for index, row in anime_data.iterrows():
        row_dict = {
            'Id': row['anime_id'],
            'Name': row['Name'],
            'English name': row['English name'],
            'Score': row['Score'],
            'Genres': row['Genres'],
            'Synopsis': row['Synopsis'],
            'Type': row['Type'],
            'Studios': row['Studios'],
            'Source': row['Source'],
            'Popularity': row['Popularity'],
            'Favorites': row['Favorites'],
            'Scored By': row['Scored By'],
            'Members': row['Members'],
        }
        updated_dict_list.append(row_dict)

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data


def anime_aired():
    data['Aired Year'] = data['Aired'].str.extract(r'(\d{4})').astype(float)
    anime_per_year = data['Aired Year'].value_counts().sort_index()

    updated_dict_list = []

    updated_dict_list.append(anime_per_year.to_dict())

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data


def top10_popular():
    new_data = data[['Name', 'Popularity']].sort_values('Popularity', ascending=False)[:10]
    new_data.set_index('Name', inplace=True)
    updated_dict_list = []

    updated_dict_list.append(new_data.to_dict())

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data


def top20_favorite():
    new_data = data[['Name', 'Favorites']].sort_values('Favorites', ascending=False)[:20]
    new_data.set_index('Name', inplace=True)
    updated_dict_list = []

    updated_dict_list.append(new_data.to_dict())

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data


def top_20_pop():
    new_data = data[['Name', 'Popularity']].sort_values('Popularity', ascending=False)[:20]

    updated_dict_list = []

    updated_dict_list.append(new_data.set_index('Name').to_dict())

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data


