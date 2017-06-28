# encoding: utf-8
import pandas as pd
import math
import sys
from utils import *
import random

for line in sys.stdin:
	selection_str = line
	selection_list = selection_str.strip().split()
"""
selection_str = "Action Musical Western"
selection_list = selection_str.strip().split()
"""
num_genres = len(selection_list)
num_per_genre = int(math.ceil(20 / num_genres))
movie_ids = set()

df = pd.read_csv('scripts/data/top20bygenre.csv')

ids_in_genre = set(df[(df.genre == selection_list[0]) | (df.genre == selection_list[1])  | (df.genre == selection_list[2])]['movieID'].tolist())
movie_ids = random.sample(ids_in_genre, 20)

#movie_ids = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
#movie_ids = ["30816"]
movies_map = build_map()
for id in movie_ids:
    id = str(id)
    #print id
    temp_list = movies_map[id]
    omdb_object = build_omdb_object(temp_list[1])
    movie_id = str(id)
    movie_name = temp_list[0]
    #movie_name = movie_name.decode('utf-8').encode('utf-8', 'ignore')
    if type(movie_name) == unicode:
        movie_name = movie_name.encode('utf-8')
    #print movie_name 
    movie_description = omdb_object["plot"]
    #movie_description = movie_description.decode('utf-8').encode('utf-8', 'ignore')
    if type(movie_description) == unicode:
        movie_description = movie_description.encode('utf-8')
    #print movie_description
    movie_image = omdb_object["poster"]
    movie_id_imdb = "none"
    #print "length of movies: %d" % len(movie_ids)
    #print '%s\t%s\t%s\t%s\t%s' % (movie_id,'\t', movie_name, movie_description, movie_image, movie_id_imdb)
    print movie_id, '\t', movie_name, '\t', movie_description, '\t', movie_image, '\t', movie_id_imdb
