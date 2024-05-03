from collections import Counter
import requests
from bs4 import BeautifulSoup

#Function that retrieves all the liked movies under a given user's letterboxd public profile. 
def get_watched(username):
    # Tries to get the html of the user's liked movies page, catches the exception if the page is not found.
    try:
        url = f'https://letterboxd.com/{username}/likes/films/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        return e    
    #finds all the movie posters on the page and extracts the movie title from the alt text of the image.
    images = soup.find_all(class_='image')
    movies = [image.get('alt') for image in images]

    #iterates through at most 10 pages of the user's liked movies. if there is no next page, then the loop is broken.
    for i in range(10):
        try:
            url = f'https://letterboxd.com/{username}/likes/films/page/{i+2}/'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            break
        images = soup.find_all(class_='image')
        current_movies = [image.get('alt') for image in images]
        #extends the total movies list to include each page of movies.
        movies.extend(current_movies)
    return movies 

#Function to get all the genres and themes of a list of movies.
def get_movie_genres(movies) :
    #Inititalize a list for each list of genres and themes. Initialize a dictionary to store the genres and themes of each movie.
    genres_total = []
    themes_total = []
    my_dict = {}

    for movie in movies:
        # process the title to be used in the url.
        formatted_movie = movie.lower().replace(' ', '-')
        url = f'https://letterboxd.com/film/{formatted_movie}/genres/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # get genres
        genre_themes_parent = soup.find(id='tab-genres')
        try:
            div_elements = genre_themes_parent.find_all('div')
        except AttributeError:
            continue

        #Get the second div element and find all the genres within the tab
        
        genre_tab = genre_themes_parent.find('div', class_= 'text-sluglist capitalize')
        genre_tags = genre_tab.find_all(class_='text-slug') 
        genres = [tag.text.strip() for tag in genre_tags]
        genres_total.extend(genres) 

        #if more than one div element is found, then the movie has themes.
        if len(div_elements) > 1:
            theme_tab = genre_tab.find_next_sibling('div', class_= 'text-sluglist capitalize')
            theme_tags = theme_tab.find_all(class_='text-slug')
            themes = [tag.text.strip() for tag in theme_tags]
            #in the webpage, an element with the text 'Show All…' is present in the themes list. This is removed.
            str = 'Show All…'
            while str in themes:
                themes.remove(str)
            themes_total.extend(themes)
            my_dict[movie] = [genres, themes]
        else:
            #only assign the genres to the movie if there are no themes.
            my_dict[movie] = [genres]

    return genres_total, themes_total, my_dict

#Function that counts the number of times each item appears in a list and returns the n most common items.
def count_items(items_list, n):
    counter = Counter()
    counter.update(items_list)
    c = counter.most_common(n)
    strings = [s[0] for s in c]
    return strings

#Function that returns the top 6 themes for each genre in a list of genres.
def corresponding_themes(genres, my_dict):
    genre_themes = {}  # Dictionary to store themes for each genre
    for genre in genres:
        themes = []
        for movie, genre_nthemes in my_dict.items():
            if(len(genre_nthemes) == 2): #if the movie has themes in the dictionary
                genre_list, themes_list = genre_nthemes #unpack the genre and themes
                if genre in genre_list:                        
                    themes.extend(themes_list) #if the current genre is found in the list of genres for each movie, add those themes to the list.
        top_themes = count_items(themes, 6)
        genre_themes[genre] = top_themes
    return genre_themes

