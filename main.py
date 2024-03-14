# import all libraries and packages
import tkinter as tk
import random
import PIL.Image
import PIL.ImageTk
# import Recommender classes
from recommenders import Recommender, CF_Recommender, KBF_Recommender, Random_Top_Recommender
# Main class definition
class Menu:
  # function with defintions of program and recalled variables
  def __init__(self, width, height):
    self.height = width
    self.width = height
    self.GENRES = ['War', 'Adventure', 'Comedy', 'Crime', 'Western', 'Animation', 'Children', 'Film-Noir', 'Sci-Fi', 'Mystery', 'Horror', 'Fantasy', 'Musical', 'IMAX', 'Romance', 'Drama', 'Thriller', 'Action', 'Documentary']
    self.counter_kbf_questions = 0
    # Create Recommenders
    self.Random_Recommender = Recommender()
    self.CF_Recommender = CF_Recommender()
    self.KBF_Recommender = KBF_Recommender()
    self.Random_Top_Recommender = Random_Top_Recommender()
    # Create widgets for main menu
    self.window = tk.Tk("Movie Recommender")
    self.window.geometry("960x720")
    # Load image
    img = PIL.Image.open("new_bg_image.png")
    img = PIL.ImageTk.PhotoImage(img)
    # Create canvas
    self.canvas = tk.Canvas(self.window)
    self.canvas.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
    self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
    # Create widgets for CF
    lbl_enter_movie = tk.Label(self.canvas, text="Enter a movie title")
    self.ent_movie_title = tk.Entry(self.canvas)
    self.btn_get_cf_recommendations = tk.Button(self.canvas, text="Get recommendations", command=self.get_recommendations_cf)
    self.lbl_display_recommendations = tk.Label(self.canvas, wraplength=800)
    #Display widgets for CBF
    lbl_enter_movie.place(anchor=tk.CENTER, x=480, y=180)
    self.ent_movie_title.place(anchor=tk.CENTER, x=480, y=210)
    self.btn_get_cf_recommendations.place(anchor=tk.CENTER, x=480, y=240)
    self.lbl_display_recommendations.place(anchor=tk.CENTER, x=480, y=270)
    # Create widgets for KBF popup
    self.lbl_kbf_question = None
    self.lbl_kbf_recommendations = None
    # Create widgets for KBF
    self.btn_open_popup_kb = tk.Button(self.canvas, text="Open popup!", command=self.open_popup_kbf)
    # display widgets for KBF
    self.btn_open_popup_kb.place(anchor=tk.CENTER, x=480, y=300)
    #button for get random recommendation
    self.btn_get_random_rec = tk.Button(self.canvas, text="Get Randomised Rec", command=self.get_random_movies_btn)
    #display widgets for random recommendation
    self.btn_get_random_rec.place(anchor=tk.CENTER, x=480, y=330)
    #button for top rated recommendation
    self.btn_getTOP_RATED_rec = tk.Button(self.canvas, text="Get the top rated movies", command=self.get_top_recommendations)
    self.lbl_top_rated = tk.Label(self.canvas, wraplength=400)
    # display widgets for top rated
    self.lbl_top_rated.place(anchor=tk.CENTER, x=480, y=360)
    self.btn_getTOP_RATED_rec.place(anchor=tk.CENTER, x=480, y=390)
    # help button
    tk.Button(self.window, text="Help", command=self.open_popup_help).place(anchor=tk.NE, x=940, y=10)
    # Quit button
    tk.Button(self.window, text="Quit", command=self.window.destroy).place(anchor=tk.CENTER, x=480, y=420)
    #display
    self.window.mainloop()

  #Popup class
  class Popup:
    def __init__(self, parent, window_title, width, height):
      self.popup = tk.Toplevel(parent)
      self.popup.geometry(str(width) + "x" + str(height))
      self.popup.title(window_title)
  
    def get_popup_window(self):
      return self.popup

  #get recommendation for CF  
  def get_recommendations_cf(self):
    movie_title = self.ent_movie_title.get()
    if self.CF_Recommender.check_movie_exists(movie_title):
      lst = self.CF_Recommender.get_recommendations(movie_title)
      self.lbl_display_recommendations["text"] = ", ".join(lst)
    else:
        self.lbl_display_recommendations["text"] = "Sorry, your movie is not in the dataset"

  #yes button function
  def yes_btn_pressed(self):
    filtered = self.KBF_Recommender.filter(self.GENRES[self.counter_kbf_questions])
    if filtered:
      self.counter_kbf_questions = self.counter_kbf_questions + 1
      self.lbl_kbf_question["text"] = "Do you like " + self.GENRES[self.counter_kbf_questions] + " movies?"
    else:
      self.lbl_kbf_recommendations["text"] = "Too much filtering, pressed the Get recommendation button"
      
  #no button function
  def no_btn_pressed(self):
      self.counter_kbf_questions = self.counter_kbf_questions + 1
      self.lbl_kbf_question["text"] = "Do you like " + self.GENRES[self.counter_kbf_questions] + " movies?"

  #get recommendation for KBF
  def get_recommendations_kbf(self):
    lst = self.KBF_Recommender.get_recommendations()
    self.lbl_kbf_recommendations ["text"] = ", ".join(lst)

  #open popup for KBF
  def open_popup_kbf(self):
    random.shuffle(self.GENRES)
    popup = self.Popup(self.window, "Knowledge Based Filtering", 250, 250)
    popup_window = popup.get_popup_window()
    # 
    self.lbl_kbf_question = tk.Label(popup_window, text="Do you like " + self.GENRES[self.counter_kbf_questions] + " movies?")
    self.lbl_kbf_question.pack()
    tk.Button(popup_window, text="Yes", command=self.yes_btn_pressed).pack()
    tk.Button(popup_window, text="No", command=self.no_btn_pressed).pack()
    tk.Button(popup_window, text="Get recommendation", command=self.get_recommendations_kbf).pack()
    self.lbl_kbf_recommendations = tk.Label(popup_window, text="", wraplength=250)
    self.lbl_kbf_recommendations.pack()
    tk.Button(popup_window, text="Quit", command=popup_window.destroy).pack()

  #open popup for KBF
  def open_popup_help(self):
    popup = self.Popup(self.window, "Help", 250, 250)
    popup_window = popup.get_popup_window()
    # 
    tk.Label(popup_window, text="Explain here").pack()
    tk.Button(popup_window, text="Quit", command=popup_window.destroy).pack()
    

  def get_top_recommendations(self):
    movie = self.Random_Top_Recommender.get_recommendations()
    self.lbl_top_rated["text"] = movie
  
  def get_random_movies_btn(self):
    lst = self.Random_Recommender.get_recommendations(self.Random_Recommender.df, num_rec=2)
    self.lbl_top_rated["text"] = ", ".join(lst)


if __name__ == "__main__":
    Menu(960, 720)
