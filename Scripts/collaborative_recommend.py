import numpy as np
import json
import math
from scipy import sparse
from scipy.sparse import csr_matrix
import yaml
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import cosine_similarity
import heapq

data_path = "scripts/data/"

def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])

def collaborative_recommend_method(rated_dict):
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
	try:
	    key = key.strip()
            movie_index = movie_id_index[key]
            col.append(movie_index)
            data.append(float(value))
	except:
	    continue

    user_rate = coo_matrix((data, (row,col)), shape=(1, 10197)).tocsr()
    similarities = csr_matrix(cosine_similarity(user_rate, rating_sparse))
    predict_rating = csr_matrix.dot(similarities, rating_sparse)

    predict_rating_sorted = predict_rating.getrow(0).toarray().ravel() #sort predicted rating result
    predict_rating_top = heapq.nlargest(20, range(len(predict_rating_sorted)), predict_rating_sorted.__getitem__) #fetch top 20 movies
    predict_rating_top_mapped = list(map(lambda x: movie_index_id[str(x)], predict_rating_top))
    predict_rating_top_selected = list(filter(lambda x: x not in list(map(lambda x: x.strip(), rated_dict.keys())), predict_rating_top_mapped))
    predict_rating_top_final = predict_rating_top_selected[:10]

    return predict_rating_top_final

if __name__ == "__main__":
    rated_movies = {"45": "5", "1721": "3", "4201": "5", "7285": "2", "8972": "1", "51662": "1", "52245": "5",
                    "52458": "1", "52722": "4", "53121": "4", "56788": "2", "54001": "5", "54004": "3", "54272": "1",
                    "54286": "1", "54734": "2", "55765": "3", "56174": "3", "56757": "5", "60072": "5"}
    collaborative_recommend(rated_movies)
    print "a"
