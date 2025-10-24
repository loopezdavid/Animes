import pandas as pd
from tabulate import tabulate

# 1️⃣ Cargar CSVs
anime_cols = ['anime_id', 'name', 'genre', 'type', 'episodes', 'anime_rating', 'members']
ratings_cols = ['user_id', 'anime_id', 'user_rating']

anime = pd.read_csv('anime.csv', names=anime_cols, header=0, encoding='utf-8')
ratings = pd.read_csv('rating.csv', names=ratings_cols, header=0, encoding='utf-8')

# 2️⃣ Unir ambos dataframes por el campo 'anime_id'
merged = pd.merge(ratings, anime, on='anime_id')

# 3️⃣ Seleccionar solo las columnas deseadas
final = merged[['anime_id', 'name', 'anime_rating', 'user_id', 'user_rating']]

# 4️⃣ Mostrar las primeras filas con tabulate
print(tabulate(final.head(10), headers='keys', tablefmt='fancy_grid', showindex=False))
