import os
import sys
from scipy import sparse
import numpy as np
import heapq
import json
from rand_walk import random_walk
from retrieve_url import submit_url
from user_profile import update_user_profile
from correlations import sparse_corrcoef
from scipy.sparse import csr_matrix
from heapq import nlargest
from utils import *

### file names and paths
data_path = "scripts/data"
#data_path = "data"
#crr_mtx_fname = "crr_mtx_1000_normalized"
#moviefname = "movie_json_1000_test"
precalc_movies_fname = "precalculated_implicit_explicit_correlations.json"

### parameters
num_features = 16529
k = 10
precalc_movies = json.load(open(os.path.join(data_path, precalc_movies_fname)))
#print precalc_movies.keys()
all_movie_ids = precalc_movies[precalc_movies.keys()[0]].keys()
#movie_implicit_profiles = json.load(open(os.path.join(data_path, movie_implicit_fname)))
### get ratings from standard input and construct user profile
ratings = []
rated_ids = []
#user_profile = [0] * num_features

for line in sys.stdin:
    rated_movies = json.loads(line)
    #rated_ids = set(rated_movies.keys())

#rated_movies = {"6380 ":"5","53894 ":"4","45950 ":"3","60763 ":"4","5669 ":"4","8622 ":"4","7156 ":"4","59126 ":"2","5224 ":"3","7256 ":"2","60766 ":"2","33677 ":"2","34072 ":"3","27873 ":"4","6299 ":"5","34153 ":"4","54881 ":"3","2323 ":"2","61236 ":"1","34542 ":"2"}

#user_profile = sparse.rand(1, num_features)

correlations = {}
for movie_id in all_movie_ids:
    correlation = 0
    for rated_id, rating in rated_movies.items():
	#print rated_id, movie_id
	rated_id = rated_id.strip()
        precalc_corr = precalc_movies[rated_id][movie_id]
        if np.isnan(precalc_corr):
            continue
	try:
            correlation += (float(rating) - 2.5) * precalc_corr
	except:
	    continue
    correlations[movie_id] = correlation


rec_ids = nlargest(k, correlations, correlations.get)

### output results
#rec_ids = ["1"]
movies_map = build_map()
for id in rec_ids:
    temp_list = movies_map[id]
    omdb_object = build_omdb_object(temp_list[1])
    movie_id = str(id)
    movie_name = temp_list[0]
    if type(movie_name) == unicode:
        movie_name = movie_name.encode('utf-8') 
    movie_description = omdb_object["plot"]
    if type(movie_description) == unicode:
        movie_description = movie_description.encode('utf-8')
    movie_image = omdb_object["poster"]
    movie_id_imdb = "none"
    print movie_id, '\t', movie_name, '\t', movie_description, '\t', movie_image, '\t', movie_id_imdb
