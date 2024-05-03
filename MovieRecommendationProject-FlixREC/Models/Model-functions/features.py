import text_processing
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def key_word_extracter(processed_text):
    # Extract key words from the processed text
    key_words = processed_text.split()

    return key_words


def genre_identifier(key_words):
    # Identify genres from the key words
    # obviously use the actual dataset we have to do this
    genres = ["action", "comedy", "drama", "horror", "romance", "sci-fi"]
    present_genres = [genre for genre in genres if genre in key_words]

    return present_genres


def trope_identifier(key_words):
    # Identify tropes from the key words
    tropes = [
        "love triangle",
        "underdog",
        "fish out of water",
        "rags to riches",
        "buddy cop",
    ]
    present_tropes = [trope for trope in tropes if trope in key_words]

    return present_tropes


def rating_tester(key_words):
    # Test the ratings of the movie
    ratings = ["PG", "PG-13", "R"]
    rating = [rating for rating in ratings if rating in key_words]

    return rating
