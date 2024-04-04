import pandas as pd
import json

anime = pd.read_csv('anime.csv')

data = anime.head(20)

dict = {
    'Title': ["Sousou no FrierenFrieren: Beyond Journey's End",
            'Fullmetal Alchemist: Brotherhood',
            'Steins;Gate',
            'Gintama°Gintama Season 4',
            'Shingeki no Kyojin Season 3 Part 2Attack on Titan Season 3 Part 2',
            'Gintama: The FinalGintama: The Very Final',
            'Hunter x Hunter (2011)Hunter x Hunter',
            'Bleach: Sennen Kessen-henBleach: Thousand-Year Blood War',
            "Gintama'Gintama Season 2",
            "Gintama': EnchousenGintama: Enchousen",
            'Kaguya-sama wa Kokurasetai: Ultra RomanticKaguya-sama: Love is War - Ultra Romantic',
            'Ginga Eiyuu DensetsuLegend of the Galactic Heroes',
            'Fruits Basket: The FinalFruits Basket: The Final Season',
            'Gintama.Gintama Season 5',
            'Gintama',
            'Shingeki no Kyojin: The Final Season - Kanketsu-henAttack on Titan: Final Season - The Final Chapters',
            'Koe no KatachiA Silent Voice',
            'Clannad: After Story',
            '3-gatsu no Lion 2nd SeasonMarch Comes In Like a Lion 2nd Season',
            'Code Geass: Hangyaku no Lelouch R2Code Geass: Lelouch of the Rebellion R2'],
    'URL' : ['https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx154587-n1fmjRv4JQUd.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx5114-KJTQz9AIm6Wk.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx21624-szbmwyC3sJos.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx20996-kBEGEGdeK1r7.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx20691-dnv0rkpbgBDJ.png',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx20996-kBEGEGdeK1r7.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx13271-jBxQFqHCpb2K.png',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx2889-AmnSwChuAuGT.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx97889-NWQVqODOuBqI.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx97889-NWQVqODOuBqI.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx125367-bl5vGalMH2cC.png',
             'https://cdn.myanimelist.net/images/anime/6/22500l.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx124194-pWfBqp3GgjOx.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx99714-0pCKHe4XYIz7.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx99714-0pCKHe4XYIz7.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx20691-dnv0rkpbgBDJ.png',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx20954-UMb6Kl7ZL8Ke.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx4181-V1LCtX1rJgbR.png',
             'https://cdn.myanimelist.net/images/anime/1325/96912l.jpg',
             'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx97880-sZWHViJfrvXm.jpg',
            ]
}

url = pd.DataFrame(dict)

data = data.merge(url, on='Title')


def topAiring():
    updated_dict_list = []

    for index, row in data.iterrows():
        row_dict = {
            'URL': row['URL'],
            'Title': row['Title'],
            'Score': str(row['Score']),
            'Status': row['Status'],
            'Popularity': str(row['Popularity']),
            'Studios': row['Studios'],
            'Episodes': str(row['Episodes'])
        }
        updated_dict_list.append(row_dict)

    json_data = json.dumps(updated_dict_list, indent=4)

    return json_data  # Yaha return kar rahe hain instead of print