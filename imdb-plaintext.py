# requirements: python 3; imdbpy
# install like: sudo pip install IMDbpy

import sys
from imdb import IMDb

print ("Please wait, fetching film data...")
i = IMDb()
for x in range(1, len(sys.argv)):
    print ('parsing ' + str(x) + ' of ' + str(len(sys.argv)-1))
    s = i.search_movie(sys.argv[x])
    m = i.get_movie(s[0].movieID)
    i.update(m, ['main', 'vote details'])
    genres = ", ".join( m['genre'] )
    print ( str(m['title']) + ': ' + str(m['rating']) + ' (' + str(m['genre']) + ')' + ', ' + str(m['year']) )
print ('Done!')
