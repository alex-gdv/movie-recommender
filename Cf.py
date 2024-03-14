import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from data_prep import data_prep_cf
  
def collaborative_filtering(movieTitle):
  movies_ratings_std = data_prep_cf()
  #get the item similarity through the function of cosine similarity 
  item_similarity = cosine_similarity(movies_ratings_std.loc[movieTitle].values.reshape(1,-1), movies_ratings_std.drop(index=movieTitle))
  #drop the target movie so it's not present in the last line
  movies_ratings_std = movies_ratings_std.drop(index=movieTitle)
  #sort movies to get the movies with the highest score and 
  item_similarity_indices = np.argsort(item_similarity).squeeze()
  #we get the most similar movie in movies_ratings_std using the last item of item_similarity_indicies which is the index of the greatest score in item_similarity.
  top_movies = []
  for i in range(1, 5):
    top_movies.append(movies_ratings_std.iloc[item_similarity_indices[-i]].name)

  #avg_highly_rated_movies = movies_ratings_std.groupby(['movieTitle']).agg({"rating": "mean"})['rating'].sort_values(ascending=False)
  #popular_movies = movies_ratings_std.groupby(['movieTitle']).agg({"rating": "count"})['rating'].sort_values(ascending=False)
  #print(popular_movies.shape)
  #return top_movies

collaborative_filtering("Toy Story (1995)")