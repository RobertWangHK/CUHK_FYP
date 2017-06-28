import numpy as np
import json
import sys
import math
from scipy import sparse
from scipy.sparse import csr_matrix
import yaml
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import cosine_similarity
import heapq
from utils import *

data_path = "scripts/data/"

def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])

def collaborative_recommend(rated_dict):
    rating_sparse = load_sparse_csr(data_path + "user_rating_matrix_sparse.npz")
    with open(data_path + "movie_id_index", "r") as input:
        movie_id_index = yaml.safe_load(input)
    input.close()
    with open(data_path + "movie_index_id", "r") as input:
        movie_index_id = yaml.safe_load(input)
    input.close()

    col = []
    row = np.zeros(20)
    data = []

    for key, value in rated_dict.items():
        key = key.strip()
        movie_index = movie_id_index[key]
        col.append(movie_index)
        data.append(float(value))

    user_rate = coo_matrix((data, (row,col)), shape=(1, 10197)).tocsr()
    similarities = csr_matrix(cosine_similarity(user_rate, rating_sparse))
    predict_rating = csr_matrix.dot(similarities, rating_sparse)

    predict_rating_sorted = predict_rating.getrow(0).toarray().ravel() #sort predicted rating result
    predict_rating_top = heapq.nlargest(20, range(len(predict_rating_sorted)), predict_rating_sorted.__getitem__) #fetch top 20 movies
    predict_rating_top_mapped = list(map(lambda x: movie_index_id[str(x)], predict_rating_top))
    predict_rating_top_selected = list(filter(lambda x: x not in list(map(lambda x: x.strip(), rated_dict.keys())), predict_rating_top_mapped))
    predict_rating_top_final = predict_rating_top_selected[:10]

    return predict_rating_top_final

for line in sys.stdin:
    rated_movies = json.loads(line)
    #rated_ids = set(rated_movies.keys())
rec_ids = collaborative_recommend(rated_movies)
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

if __name__ == "__main__":
    rated_movies = {"5888 ":"5","61323 ":"4","37733 ":"3","8798 ":"2","58559 ":"4","41285 ":"5","6874 ":"3","51540 ":"4","55765 ":"5","49530 ":"3","54997 ":"2","33794 ":"4","48516 ":"3","39292 ":"5","5956 ":"4","6157 ":"3","5464 ":"2","55820 ":"4","5445 ":"5","1805 ":"4"}
    rec_ids = collaborative_recommend(rated_movies)
    print rec_ids

