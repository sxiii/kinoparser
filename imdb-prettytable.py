# requirements: python 3; imdbpy; prettytable
# install like: sudo pip install IMDbpy PrettyTable
# comments below are to support printing without prettytable

import sys
from imdb import IMDb
from prettytable import PrettyTable
t = PrettyTable()
t.field_names = ["Title", "Year", "Rating", "Genres"]

print ("Please wait, fetching film data...")
i = IMDb()
for x in range(1, len(sys.argv)):
    print ('parsing ' + str(x) + ' of ' + str(len(sys.argv)-1))
    s = i.search_movie(sys.argv[x])
    m = i.get_movie(s[0].movieID)
    i.update(m, ['main', 'vote details'])
    #print ( str(m['title']) + ': ' + str(m['rating']) + ' (' + str(m['genre']) + ')' + ', ' + str(m['year']) )
    genres = ", ".join( m['genre'] )
    t.add_row([ str(m['title']), str(m['year']), str(m['rating']), genres ])
print ('Done!')
#print (t)
print (t.get_string(sortby="Rating"))
