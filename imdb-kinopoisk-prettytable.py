# requirements: python 3; imdbpy; prettytable; kinopoisk
# install like: sudo pip install IMDbpy PrettyTable kinopoiskpy

import sys
from imdb import IMDb
from prettytable import PrettyTable
from kinopoisk.movie import Movie

t = PrettyTable()
t.field_names = ["Title", "Year", "IMDb Rating", "Kinopoisk Rating", "Total Rating", "Genres", "Countries", "Runtime", "URL"]

print ("Please wait, fetching film data...")
i = IMDb()
for x in range(1, len(sys.argv)):
    print ('parsing ' + str(x) + ' of ' + str(len(sys.argv)-1))
    s = i.search_movie(sys.argv[x])
    m = i.get_movie(s[0].movieID)
    i.update(m, ['main', 'vote details'])
    movie_list = Movie.objects.search(sys.argv[x])
    genres = ", ".join(m['genre'])
    countries = ", ".join(m['countries'])
    runtimes = ", ".join(m['runtimes'])
    filmurl = "https://imdb.com/title/tt" + str(s[0].movieID)
    totalrate = m['rating']+movie_list[0].rating
    t.add_row([ str(m['title']), str(m['year']), str(m['rating']), movie_list[0].rating, totalrate, genres, countries, runtimes, filmurl ])
print ('Done!')
print (t.get_string(sortby="IMDb Rating"))
