import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
import pickle
import numpy as np

#Load all previously trained models
def load():
    global tfidf_vectorizer
    global tfidf_matrix_summaries
    global movies_data_cleaned
    global genre_list
    tfidf_vectorizer = pickle.load(
        open("Models/saved_weights/tfidf_vectorizer.pkl", "rb")
    )
    tfidf_matrix_summaries = pickle.load(
        open("Models/saved_weights/tfidf_matrix_summaries.pkl", "rb")
    )
    movies_data_cleaned = pd.read_csv("Models/saved_weights/movies_data_cleaned.csv")
    genre_list = movies_data_cleaned.genre_1.unique() 
    print(len(genre_list))

#For a given plot, extract only the keywords from it
def get_keywords(plot):
    # vectorize the given plot
    plot_tfidf = tfidf_vectorizer.transform([plot])
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # retrieve the keyword importance for each word
    scores = dict({(feature_names[i], plot_tfidf[0, i]) for i in plot_tfidf.indices})
    keywords = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [k[0] for k in keywords]

#Recommend movies based on the input plot and according to a given streaming service
def recommend_movies_based_on_input_plot(input_plot, streaming):
    #vectorize the input plot
    input_vec = tfidf_vectorizer.transform([input_plot])
    #filter movies based on streaming service
    filtered_movies = movies_data_cleaned['service'].apply(lambda s: s in streaming)
    filtered_movies_data = movies_data_cleaned[filtered_movies]

    #if there are movies in the filetered data, calculate the cosine similarity between the input plot and the filtered movies
    if not filtered_movies_data.empty:
        #extract only the tf-idf scores of the filtered movies
        filtered_tfidf_matrix = tfidf_matrix_summaries[filtered_movies_data.index]
        cosine_sim = cosine_similarity(input_vec, filtered_tfidf_matrix)
        #Sort similarity scores in descending order
        sim_scores = list(enumerate(cosine_sim[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:5]
        movie_indices = [i[0] for i in sim_scores]
        
        #Randly select one of the movies from the top 5 similar movies
        recommend_movie = np.random.choice(list(movies_data_cleaned["title"].iloc[movie_indices]))
        response_str = f"I would recommend you check out {recommend_movie}"
        return response_str

#Recommend movies based on the input genre and according to a given streaming service
def recommend_movies_based_on_genre(input_genre, streaming):
    genre_keywords = get_keywords(input_genre)
    input_vec = tfidf_vectorizer.transform([input_genre])

    # see if any of the keywords match a genre
    genre_det = ""
    fuzz_score = -1    
    for potential_genre in genre_keywords:
        for genre in genre_list:
            curr_score = fuzz.ratio(str(potential_genre), str(genre))
            if(curr_score > 80 and curr_score > fuzz_score):
                genre_det = genre 
                fuzz_score = curr_score 

    print(f"genre det: {genre_det}")
    
    genre_columns = ['genre_1', 'genre_2', 'genre_3', 'genre_4', 'genre_5', 'genre_6', 'genre_7'] 
    filtered_movies = movies_data_cleaned[genre_columns].apply(lambda x: x.str.contains(genre_det, case=False, na=False)).any(axis=1)
    filtered_movies_data = movies_data_cleaned[filtered_movies]

    filtered_movies = filtered_movies_data['service'].apply(lambda s: s in streaming)
    filtered_movies_data = filtered_movies_data[filtered_movies]

    recommend_movie = ""
    if not filtered_movies_data.empty:
        filtered_tfidf_matrix = tfidf_matrix_summaries[filtered_movies_data.index]
        cosine_sim = cosine_similarity(input_vec, filtered_tfidf_matrix)
        sim_scores = list(enumerate(cosine_sim[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:5]
        movie_indices = [i[0] for i in sim_scores]
        recommend_movie = np.random.choice(list(movies_data_cleaned["title"].iloc[movie_indices]))
    else:
        return "No movies found in the preferred genre :("
    
    return f"I think you should try out {recommend_movie}!"


## TODO: Extract movie names and then do it based on similarity 
def get_similar_keywords(input):
    # vectorize the given genre
    input_tfidf = tfidf_vectorizer.transform([input])
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # retrieve the keyword importance for each word
    scores = dict({(feature_names[i], input_tfidf[0, i]) for i in input_tfidf.indices})
    keywords = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [k[0] for k in keywords]


def recommend_movies_based_on_similarity(input):
    sim_keywords = get_similar_keywords(input)
    print(sim_keywords)
    input_vec = tfidf_vectorizer.transform([input])
    cosine_sim = cosine_similarity(input_vec, tfidf_matrix_summaries)
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies_data_cleaned["title"].iloc[movie_indices]
