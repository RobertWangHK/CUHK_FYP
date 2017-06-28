import numpy as np
from scipy.stats import pearsonr
from scipy.sparse import csr_matrix
import json
from math import sqrt
from scipy import sparse
#from sklearn.metrics.pairwise import cosine_similarity

def sparse_corrcoef(A, B=None):

    if B is not None:
        A = sparse.vstack((A, B), format='csr')

    A = A.astype(np.float64)

    # compute the covariance matrix
    # (see http://stackoverflow.com/questions/16062804/)
    A = A - A.mean(1)
    norm = A.shape[1] - 1.
    C = A.dot(A.T.conjugate()) / norm

    # the correlation coefficients are given by
    # C_{i,j} / sqrt(C_{i} * C_{j})
    d = np.diag(C)
    coeffs = C / np.sqrt(np.outer(d, d))

    return coeffs
def sparse_pearsonr(a, b):
    length = a.shape[1]
    mean_a = a.mean()
    mean_b = b.mean()
    mean_product_ab = mean_a * mean_b
    mean_product_aa = mean_a ** 2
    mean_product_bb = mean_b ** 2
    am = a - np.Array([a.mean()] * length)
    bm = b - np.Array([b.mean()] * length)
    return cosine_similarity(am, bm)
    
def get_correlarion_dict(profile_dict1, profile_dict2):
	correlation_dict = {}
	id_list1 = profile_dict1.keys()
	id_list2 = profile_dict2.keys()
	for i, id1 in enumerate(id_list1):
		if i % 100 == 0:
		    print i
		profile1 = csr_matrix(profile_dict1[id1])
		correlation_dict[id1] = {}
		for id2 in id_list2:
			profile2 = csr_matrix(profile_dict2[id2])
			correlation_dict[id1][id2] = sparse_corrcoef(profile1, profile2)[0, 1]
	return correlation_dict

if __name__ == '__main__':
    
    user_profiles = json.load(open("data/user_implicit_tags"))
    movie_profiles = json.load(open("data/movie_explicit_tags"))

    corr_dict = get_correlarion_dict(user_profiles, movie_profiles)
    with open("data/user_implicit_movie_explicit_correlations.json", 'w') as out:
       json.dump(corr_dict, out)
    
    user_profiles = json.load(open("data/user_explicit_tags"))
    #movie_profiles = json.load(open("data/movie_explicit_tags"))

    corr_dict = get_correlarion_dict(user_profiles, movie_profiles)
    with open("data/user_explicit_movie_explicit_correlations.json", 'w') as out:
       json.dump(corr_dict, out)




"""
movie_implicit_profiles = json.load(open("data/movie_implicit_tags"))
movie_explicit_profiles = json.load(open("data/movie_explicit_tags"))
movie_ids = map(int, movie_explicit_profiles.keys())
num_movies = len(movie_ids)
explicit_correlations = {}
implicit_correlations = {}

for movie_id in movie_ids:
	movie_explicit_profiles[str(movie_id)] = csr_matrix(movie_explicit_profiles[str(movie_id)])
	movie_implicit_profiles[str(movie_id)] = csr_matrix(movie_implicit_profiles[str(movie_id)])
for i in range(num_movies):
	if i % 1000 == 0:
		print i
	movie_id1 = movie_ids[i]
	explicit_correlations[movie_id1] = {}
	for j in range(i + 1, num_movies):
		movie_id2 = movie_ids[j]
		explicit_correlations[movie_id1][movie_id2] = sparse_corrcoef(movie_explicit_profiles[str(movie_id1)], movie_explicit_profiles[str(movie_id2)])[0, 1]
with open("data/movie_explicit_correlations",'w') as f:
    json.dump(explicit_correlations, f)
del explicit_correlations

k = 0
for movie_id1 in movie_ids:
	if k % 1000 == 0:
		print k
	k += 1
	implicit_correlations[movie_id1] = {}
	for movie_id2 in movie_ids:
		if movie_id1 != movie_id2:
		    implicit_correlations[movie_id1][movie_id2] = sparse_corrcoef(movie_implicit_profiles[str(movie_id1)], movie_explicit_profiles[str(movie_id2)])[0, 1]
with open("data/movie_implicit_correlations", 'w') as f:
    json.dump(implicit_correlations, f)
"""
