import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Recommender:
  def __init__(self):
    self.df = pd.read_csv("cf_data.csv").set_index("title")
  
  def get_recommendations(self, df, num_rec=5):
    #the list of recommendations variable
    lst_recommendations = []
    # nums is used to store the indices of movies that have already been chosen 
    nums = []
    # This for loop is to get 5 random movies in num_movies
    for i in range(num_rec):
        num = random.randint(0, df.shape[0] - 1)
        # 20 movies, 10, 10
        while num in nums:
            num = random.randint(0, df.shape[0] - 1)
        # nums = [10]
        nums.append(num)
        temp = df.iloc[num].name
        lst_recommendations.append(temp)
    return lst_recommendations

class CF_Recommender(Recommender):
  def __init__(self):
    super().__init__()

  def check_movie_exists(self, movie_title):
    if movie_title in self.df.index:
      return True
    return False
  
  def get_recommendations(self, movieTitle):
    print(self.df.shape)
    # get the item similarity through the function of cosine similarity
    item_similarity = cosine_similarity(self.df.loc[movieTitle].values.reshape(1, -1), self.df.drop(index=movieTitle))
    # drop the target movie so it's not present in the last line
    movies_ratings_std = self.df.drop(index=movieTitle)
    # sort movies to get the movies with the highest score and
    item_similarity_indices = np.argsort(item_similarity).squeeze()
    # we get the most similar movie in movies_ratings_std using the last item of item_similarity_indicies which is the index of the greatest score in item_similarity.
    top_movies = []
    for i in range(1, 5):
        top_movies.append(movies_ratings_std.iloc[item_similarity_indices[-i]].name)
    return top_movies
  

class KBF_Recommender(Recommender):
  def __init__(self):
    self.df = pd.read_csv("kbf_data.csv").set_index("title")
    self.df_filtered = self.df.copy()

  def filter(self, genre):
    if self.df_filtered[self.df_filtered[genre]==1].shape[0] >= 5:
      self.df_filtered = self.df_filtered[self.df_filtered[genre]==1]
      return True
    return False

  def reset_df(self):
    self.df_filtered = self.df.copy()
  
  def get_recommendations(self):
    return super().get_recommendations(self.df_filtered, 5)

class Random_Top_Recommender(Recommender):
  def __init__(self):
    self.df = pd.read_csv("ratings_data.csv").set_index("title")

  def get_recommendations(self, min_avg_rating=4, min_rating_count=10):
    random_top_movie = ""
    indices = []
    i = 0
    for index, row in self.df.iterrows():
      # row.mean() gets the average rating ignoring NaN values, row.count() counts the number of ratings
      if row.mean() > min_avg_rating and row.count() > min_rating_count:
          indices.append(i)
      i += 1
    movies_ratings_top = self.df.iloc[indices]
    random_top_movie = super().get_recommendations(movies_ratings_top, 1)[0]
    return random_top_movie
  
# x = Random_Top_Recommender().get_recommendations()
# print(x)