from bs4 import BeautifulSoup
import pprint
import urllib2, bs4
import csv
import urllib
import json

OMDB_API_URL = 'http://www.omdbapi.com'

# print json.load(urllib2.urlopen('http://www.omdbapi.com/?t=chicago'))['imdbID']
x = list()
with open('movies.csv', 'rb') as m:
  reader = csv.reader(m)
  for row in reader:
    x.append(row)

def fetch_movie_id(movie, year):
  movie = movie.replace(' ', '%20')
  return json.load(urllib2.urlopen('http://www.omdbapi.com/?t=%s&y=%s' % (movie, year)))['imdbID']

def construct_movie_url(id):
  return 'http://www.imdb.com/title/%s/ratings?ref_=tt_ov_rt' % id

def get_movie_votes_url(movie, year):
  return construct_movie_url(fetch_movie_id(movie, year))

with open("newmovies.csv", "w") as f:

  for k in range(0, len(x)):
    movie, year = x[k]
    try: 
      req = urllib2.urlopen(get_movie_votes_url(movie, year)) 
      raw = req.read()
      soup = bs4.BeautifulSoup(raw, 'html.parser')
      results =  soup.table.find_all('td', {'align' : 'right'})
      resultsAsText = map(lambda x: x.findAll(text=True)[0],results)
      movierow = ",".join([movie, year] + resultsAsText[1:][::2])

      f.write(movierow)
      f.write("\n")

    except:
      movierow = ",".join([movie, year, 'notfound'])
      f.write(movierow)
      f.write("\n")






