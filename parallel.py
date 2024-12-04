import sys
from imdb import IMDb
from prettytable import PrettyTable
from kinopoisk.movie import Movie
from concurrent.futures import ThreadPoolExecutor

# Initialize PrettyTable
t = PrettyTable()
t.field_names = ["Title", "Year", "IMDb Rating", "Kinopoisk Rating", "Total Rating", "Genres", "Countries", "Runtime", "URL"]

print("Please wait, fetching film data...")

# Function to fetch and process data for a single movie
def fetch_movie_data(movie_name):
    i = IMDb()
    
    # IMDb data retrieval
    s = i.search_movie(movie_name)
    if not s:
        print(f"Error: No results found for {movie_name}")
        return None  # Skip if no results
    
    m = i.get_movie(s[0].movieID)
    i.update(m, ['main', 'vote details'])

    # Kinopoisk data retrieval
    movie_list = Movie.objects.search(movie_name)
    
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

    # Prepare row data for the table
    return [
        str(m.get('title', 'N/A')),
        str(m.get('year', 'N/A')),
        str(m.get('rating', 'N/A')),
        getattr(movie_list[0], 'rating', 'N/A') if movie_list else 'N/A',
        totalrate,
        genres,
        countries,
        runtimes,
        filmurl
    ]

# Using ThreadPoolExecutor to fetch and process movies in parallel
with ThreadPoolExecutor() as executor:
    # Fetch movie data for all movies in parallel
    movie_data = list(executor.map(fetch_movie_data, sys.argv[1:]))

    # Add rows to the table for valid movie data
    for data in movie_data:
        if data:  # Skip any None results
            t.add_row(data)

print('Done!')
print(t.get_string(sortby="IMDb Rating"))
