# requirements: python 3; imdbpy; prettytable; kinopoisk
# install like: sudo pip install IMDbpy PrettyTable kinopoiskpy

import sys
from imdb import IMDb
from prettytable import PrettyTable
from kinopoisk.movie import Movie

t = PrettyTable()
t.field_names = ["Title", "Year", "IMDb Rating", "Kinopoisk Rating", "Total Rating", "Genres", "Countries", "Runtime", "URL"]

print("Please wait, fetching film data...")
i = IMDb()
for x in range(1, len(sys.argv)):
    print(f'parsing {x} of {len(sys.argv)-1}')
    
    # IMDb data retrieval
    s = i.search_movie(sys.argv[x])
    if not s:
        print(f"Error: No results found for {sys.argv[x]}")
        continue  # Skip to the next movie
    
    m = i.get_movie(s[0].movieID)
    i.update(m, ['main', 'vote details'])

    # Kinopoisk data retrieval
    movie_list = Movie.objects.search(sys.argv[x])
    
    # Safely handle missing data by using .get() and default values
    genres = ", ".join(m.get('genre', ['N/A']))  # Default to 'N/A' if 'genre' is missing
    countries = ", ".join(m.get('countries', ['N/A']))  # Default to 'N/A' if 'countries' is missing
    runtimes = ", ".join(m.get('runtimes', ['N/A']))  # Default to 'N/A' if 'runtimes' is missing
    filmurl = f"https://imdb.com/title/tt{str(s[0].movieID)}"  # Always valid URL for IMDb

    # Ensure movie_list[0] exists before accessing
    movie_rating = float(getattr(movie_list[0], 'rating', 0) or 0) if movie_list else 0

    # Use movie_rating in the totalrate calculation
    imdb_rating = float(m.get('rating', 0) or 0)  # Default to 0 if 'rating' is missing
    totalrate = imdb_rating + movie_rating  # Sum IMDb and Kinopoisk ratings

    # Add row to the table, with N/A placeholders where applicable
    t.add_row([
        str(m.get('title', 'N/A')),  # Default to 'N/A' if 'title' is missing
        str(m.get('year', 'N/A')),   # Default to 'N/A' if 'year' is missing
        str(imdb_rating or 'N/A'),   # Default to 'N/A' if 'rating' is missing
        getattr(movie_list[0], 'rating', 'N/A') if movie_list else 'N/A',  # Handle empty movie_list
        totalrate,  # Already calculated, no changes needed
        genres,     # Join genres or default to 'N/A'
        countries,  # Join countries or default to 'N/A'
        runtimes,   # Join runtimes or default to 'N/A'
        filmurl     # Always valid URL for IMDb
    ])

print('Done!')
print(t.get_string(sortby="IMDb Rating"))

