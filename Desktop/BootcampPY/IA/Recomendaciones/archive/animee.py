import pandas as pd

r_cols = ['anime_id', 'name', 'rating']
animes = pd.read_csv('.\\anime', sep='\t', names=r_cols, usecols=range(3), encoding="ISO-8859-1")

m_cols = ['user_id', 'anime_id']
ratings = pd.read_csv('.\\rating', sep='|', names=m_cols, usecols=range(2), encoding="ISO-8859-1")

ratings = pd.merge(animes, ratings)

print(ratings.head())