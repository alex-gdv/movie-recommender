import pandas as pd
import data_prep

def knowledge_based_filtering(movies, genre):
  movies = movies[movies[genre]==1] 
  return movies