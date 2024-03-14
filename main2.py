import tkinter as tk
import random
import PIL.Image
import PIL.ImageTk

from Cf import collaborative_filtering
from Kf import knowledge_based_filtering
from data_prep import data_prep_kb, data_prep_cf

# https://www.tutorialspoint.com/python/tk_canvas.htm

height = 960
width = 720

#list of genres that is in the movie dataset
genres = ['War', 'Adventure', 'Comedy', 'Crime', 'Western', 'Animation', 'Children', 'Film-Noir', 'Sci-Fi', 'Mystery',
          'Horror', 'Fantasy', 'Musical', 'IMAX', 'Romance', 'Drama', 'Thriller', 'Action', 'Documentary']
i = 0
#This means that you cannot call them on the same line as you create a widget.
lbl_question = None
df_movies_genres = data_prep_kb()
# pandas dataframe text column to lowercase

df_movies_ratings = data_prep_cf(standardization=False)
yes_btn_pressed = False
#This means that you cannot call them on the same line as you create a widget.
lbl_recommendations = None
df_movies_genres_temp_copy = None

def get_random_movies(df, num_movies, genres_df=True):
    lst_recommendations = []
    nums = []
    for i in range(num_movies):
        num = random.randint(0, df.shape[0] - 1)
        while num in nums:
            num = random.randint(0, df.shape[0] - 1)
        nums.append(num)
        temp = df.iat[num, 1] if genres_df else df.iloc[num].name
        lst_recommendations.append(temp)
    return lst_recommendations


def get_recommendations_kb():
    global yes_btn_pressed, df_movies_genres_temp_copy, lbl_recommendations
    if yes_btn_pressed:
        lst_recommendations = get_random_movies(df_movies_genres_temp_copy, 5)
        lbl_recommendations["text"] = ", ".join(lst_recommendations)
    else:
        pass


def yes_btn_pressed():
    global i, genres, lbl_question, df_movies_genres_temp_copy, yes_btn_pressed
    yes_btn_pressed = True
    if knowledge_based_filtering(df_movies_genres_temp_copy, genres[i]).shape[0] >= 5:
      df_movies_genres_temp_copy = knowledge_based_filtering(df_movies_genres_temp_copy, genres[i])
      i = i + 1
      lbl_question["text"] = "Do you like " + genres[i] + " movies?"
    else:
      print("too much filtering")
      get_recommendations_kb()


def no_btn_pressed():
    global i, genres, lbl_question
    i = i + 1
    lbl_question["text"] = "Do you like " + genres[i] + " movies?"


# https://www.tutorialspoint.com/how-do-i-create-a-popup-window-in-tkinter
def open_popup_kb():
    global i, genres, lbl_question, df_movies_genres, df_movies_genres_temp_copy, lbl_recommendations
    df_movies_genres_temp_copy = df_movies_genres.copy()
    top = tk.Toplevel(window)
    top.geometry("250x250")
    top.title("Child Window")
    lbl_question = tk.Label(top, text="Do you like " + genres[i] + " movies?")
    lbl_question.pack()
    tk.Button(top, text="Yes", command=yes_btn_pressed).pack()
    tk.Button(top, text="No", command=no_btn_pressed).pack()
    tk.Button(top, text="Get recommendation", command=get_recommendations_kb).pack()
    lbl_recommendations = tk.Label(top, text="", wraplength=250)
    lbl_recommendations.pack()



def get_recommendations_cf():
    movieTitle = ent_movieTitle.get()
    if (df_movies_genres["title"] == movieTitle).any() == True:
        lst = collaborative_filtering(movieTitle)
        lbl_displayMovieTitles["text"] = ", ".join(lst)
    else:
        lbl_displayMovieTitles["text"] = "Sorry"

def get_top_recommendations():
    top_movie = ""
    indices = []
    i = 0
    for index, row in df_movies_ratings.iterrows():
        if row.mean() > 4 and row.count() > 10:
            indices.append(i)
        i += 1
    movies_ratings_top = df_movies_ratings.iloc[indices]
    top_movie = get_random_movies(movies_ratings_top, 1, genres_df=False)[0]
    lbl_top_rated["text"] = top_movie
    # change text of a label to display movie title

def get_random_movies_btn():
    random_movies = get_random_movies(df_movies_genres, 1)[0]
    print(random_movies)

def resize(event):
    global height, width
    print(event.widget)
    if height != event.height or width != event.width:
        height = event.height
        width = event.width
        print(height, width)

if __name__ == "__main__":
    img = PIL.Image.open("new_bg_image.png")
    random.shuffle(genres)
    window = tk.Tk()
    window.geometry("960x720")
    # window.widget = "window"
    window.bind("<Configure>", resize)
    canvas = tk.Canvas(window)
    lbl_1 = tk.Label(canvas, text="Enter a movie title")
    ent_movieTitle = tk.Entry(canvas)
    btn_getRecommendations = tk.Button(canvas, text="Click me!", command=get_recommendations_cf)
    lbl_displayMovieTitles = tk.Label(canvas, wraplength=400)
    btn_open_popup_kb = tk.Button(canvas, text="Open popup!", command=open_popup_kb)
    btn_get_random_rec = tk.Button(canvas, text="Get Randomised Rec", command=get_random_movies_btn)
    btn_getTOP_RATED_rec = tk.Button(canvas, text="Get the top rated movies", command=get_top_recommendations)
    lbl_top_rated = tk.Label(canvas, wraplength=400)
    canvas.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
    img = PIL.ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    lbl_1.pack()
    ent_movieTitle.pack()
    btn_getTOP_RATED_rec.pack(side='left')
    btn_get_random_rec.pack(side='right')
    lbl_top_rated.pack()
    btn_getRecommendations.pack()
    lbl_displayMovieTitles.pack()
    btn_open_popup_kb.pack()
    window.mainloop()
#https://stackoverflow.com/questions/50944627/image-resize-not-working-on-photoimage-in-tkinter