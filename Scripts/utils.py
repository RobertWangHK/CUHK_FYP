import json
import collections
import omdb
import urllib

def build_map():
    with open("scripts/data/movies.dat", "r") as input:
        movies = input.read().splitlines()
        del movies[0]
    input.close()
    movies_dict = {}
    for movie_item in movies:
        movie_item = movie_item.split("\t")
        movies_dict[movie_item[0]] = [movie_item[1], movie_item[2]]
    return movies_dict

def build_omdb_object(movie_imdbid):
    return omdb.imdbid("tt" + movie_imdbid)


