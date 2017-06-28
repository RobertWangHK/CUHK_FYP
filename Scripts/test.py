from utils import *
import os

rec_ids = ["1"]

movies_map = build_map()
for id in rec_ids:
    temp_list = movies_map[id]
    omdb_object = build_omdb_object(temp_list[1])
    movie_id = str(id)
    movie_name = temp_list[0]
    movie_description = omdb_object["plot"]
    movie_image = omdb_object["poster"]
    movie_id_imdb = "none"
    a = '%s^%s^%s^%s^%s' % (movie_id, movie_name, movie_description, movie_image, movie_id_imdb)
    print a


