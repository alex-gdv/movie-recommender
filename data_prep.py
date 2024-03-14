import pandas as pd

def data_prep_kb():
  movies = pd.read_csv('movies.csv')
  # used to find all the genres in the dataset
  # genres_t = set()
  # for i in range(movies.shape[0]):
  #   genres = movies.iat[i,2]
  #   genres = genres.split("|")
  #   genres_t.update(genres)
  # print(genres_t)
  genres = ['(no genres listed)', 'War', 'Adventure', 'Comedy', 'Crime', 'Western', 'Animation', 'Children', 'Film-Noir', 'Sci-Fi', 'Mystery', 'Horror', 'Fantasy', 'Musical', 'IMAX', 'Romance', 'Drama', 'Thriller', 'Action', 'Documentary']
  for genre in genres:
    movies[genre] = 0
  # going row by row
  for i in range(movies.shape[0]):
    # get the genres of current movie
    curr_genres = movies.iat[i,2] # "Adventure|Animation|Children|Comedy|Fantasy"
    # split the string
    curr_genres = curr_genres.split("|") # [Adventure, Animation, Children, Comedy, Fantasy]
    for curr_genre in curr_genres:
      if curr_genre == "War":
        movies.iat[i,4] = 1
      elif curr_genre == "Adventure":
        movies.iat[i,5] = 1
      elif curr_genre == "Comedy":
        movies.iat[i,6] = 1
      elif curr_genre == "Crime":
        movies.iat[i,7] = 1
      elif curr_genre == "Western":
        movies.iat[i,8] = 1
      elif curr_genre == "Animation":
        movies.iat [i,9] = 1
      elif curr_genre == 'Children': 
        movies.iat [i,10] = 1
      elif curr_genre == 'Film-Noir':
        movies.iat [i,11] = 1
      elif curr_genre == "Sci-Fi":
        movies.iat[i,12] = 1
      elif curr_genre == "Mystery":
        movies.iat[i,13] = 1
      elif curr_genre == "Horror":
        movies.iat[i,14] = 1
      elif curr_genre == "Fantasy":
        movies.iat[i,15] = 1
      elif curr_genre == "Musical":
        movies.iat[i,16] = 1
      elif curr_genre == "IMAX":
        movies.iat[i,17] = 1
      elif curr_genre == "Romance":
        movies.iat[i,18] = 1
      elif curr_genre == "Drama":
        movies.iat [i,19] =1
      elif curr_genre == "Thriller":
        movies.iat[i,20] = 1
      elif curr_genre == "Action":
        movies.iat[i,21] = 1
      elif curr_genre == "Documentary":
        movies.iat[i,22] = 1
        
  movies = movies.drop(["genres", "(no genres listed)"], axis=1)
  return movies

def data_prep_cf(standardization=True):
  #load all files that are being used
  ratings = pd.read_csv('ratings.csv')
  movies = pd.read_csv('movies.csv')
  #merge the movies and ratings file, whilst dropping the rows of 'timestamp'and 'movieId'
  movies_ratings = pd.merge(movies, ratings,).drop(['timestamp', 'movieId'], axis=1)
  #chaging the interface of the movies_ratings dataframe to make it more accessible 
  movies_ratings = movies_ratings.pivot_table(index=['title'], columns=['userId'], values='rating')
  if standardization:
    #prepare the data by standaradizing the ratings 
    movies_ratings = movies_ratings.apply(standardize) 
    #replace any NaN values with 0 so the cosine similarity can be implemted
    movies_ratings = movies_ratings.fillna(0)
  return movies_ratings

def standardize(row):
  new_row = (row - row.mean()) /(row.max() - row.min())
  return new_row

df1 = data_prep_kb()
df2 = data_prep_cf()
df3 = data_prep_cf(standardization=False)

df1.to_csv("kbf_data.csv")
df2.to_csv("cf_data.csv")
df3.to_csv("ratings_data.csv")