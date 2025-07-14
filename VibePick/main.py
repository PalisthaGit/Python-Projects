import tkinter as tk
from tkinter import ttk
import random
from movie_data import options, mood_movies

root = tk.Tk()
root.geometry("600x520")
root.title("MovieVibePicker")

intro_label = tk.Label(
    root,
    text=(
        "Not sure what to watch? Pick the kind of movie you’re in the mood for—"
        "feel-good, scary, exciting, or something else—and I’ll suggest one for you."
    ),
    wraplength=550, font=('Arial', 12), anchor="w", justify="left"
)
intro_label.grid(row=0, column=1, columnspan=2, sticky="w", pady=(10, 20))

kind_label = tk.Label(root, text="What kind of movie do you want to watch?")
kind_label.grid(row=1, column=1, sticky="w")

kind_box = ttk.Combobox(root, values=options, state='readonly')
kind_box.current(0)
kind_box.grid(row=2, column=1, sticky="w", padx=(0, 20), pady=(0,10))

button = tk.Button(root, text="Suggest", command=lambda: suggest_movie())
button.grid(row=3, column=1, sticky="w", pady=(0, 15))

movie_recommendation_label = tk.Label(
    root, text="", font=('Arial', 12, 'bold'), width=60, anchor="w", justify="left"
)
movie_recommendation_label.grid(row=4, column=1, columnspan=2, sticky="w", pady=(5, 10))

recommended_movie_label = tk.Label(
    root, text="", font=('Arial', 12), width=60, anchor="w", justify="left"
)
recommended_movie_label.grid(row=5, column=1, columnspan=2, sticky="w", pady=(5, 20))

def suggest_movie():
    movie_type = kind_box.get()
    movie_recommendation_label.config(
        text=f"Here's a {movie_type.lower()} movie for you:"
    )
    movies_for_type = mood_movies.get(movie_type, ["No movie suggestion available."])
    recommended_movie = random.choice(movies_for_type)
    recommended_movie_label.config(text=recommended_movie)

root.mainloop()
