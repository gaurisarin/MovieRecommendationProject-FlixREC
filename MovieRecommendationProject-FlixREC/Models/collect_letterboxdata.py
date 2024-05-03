from Models.letterboxd import get_watched, get_movie_genres, count_items, corresponding_themes
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk


#This function collects all the genres and themes of a given letterboxd user.
def collect_letterboxd_data(user_name):
    try:
        #gets all the liked movies
        movies = get_watched(user_name)
    except Exception as e:
        return e
    #gets a list of themes, list of genres, and a dictionary of movies and their genres and themes
    genres, themes, my_dict = get_movie_genres(movies)

    #gets the top 3 genres
    top_genres = count_items(genres, 3)

    #Dictionary of genres and their corresponding top 6 themes
    g_t_dict = corresponding_themes(top_genres, my_dict)
    return top_genres, g_t_dict


    
    










