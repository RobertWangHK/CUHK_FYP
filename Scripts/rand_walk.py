import numpy as np
from scipy import spatial
from scipy import sparse



def init_vector(rated_ids, ratings, num_docs):
    p = np.zeros((num_docs, 1))
    num_rated = len(rated_ids)
    """avg_r = ratings.mean()
    new_ratings = np.array([0 if rating <= avg_r else rating for rating in ratings])
    if sum(new_ratings) == 0:
        new_ratings = np.ones(num_rated)
    new_avg_r = new_ratings.mean()
    for i in range(num_rated):
        movie_id = rated_ids[i]
        p[movie_id] = new_avg_r * new_ratings[i]"""
    for i in range(num_rated):
        movie_id = rated_ids[i]
        p[movie_id] = ratings[i] - 3

    return p

def random_walk(crr_mtx, num_docs, alpha, threshold, rated_ids, ratings):
    #print "random walking"
    #cos_distance = 1
    start_p = init_vector(rated_ids, ratings, num_docs)
    p = start_p
    new_p = np.zeros((num_docs, 1))
    euc_distance = 1
    #i = 0
    #while cos_distance >= threshold:
    while euc_distance >= threshold:
        new_p = (1 - alpha) * crr_mtx.dot(p) + alpha * start_p
        #cos_distance = spatial.distance.cosine(p, new_p)
        euc_distance = spatial.distance.euclidean(p,new_p)
        """if i % 100 == 0:
            #print "%dth iter: %f" % (i, cos_distance)
            print "%dth iter: %f" % (i, euc_distance)"""
        p = new_p
        #i += 1

    for movie_id in rated_ids:
        p[movie_id] = 0
    
    return p

#p = csc_matrix(([1],([0],[0])), shape = (num_docs, 1))
if __name__== "__main__":
    import os
    from scipy import sparse
    import numpy as np
    import heapq
    import json 
    
    data_path = "../data"
    crr_mtx_fname = "crr_mtx_1000_normalized"
    moviefname = "movie_json_1000"
    alpha = 0.5
    threshold = 1e-10
    k = 10

    dense_crr_mtx = np.loadtxt(os.path.join(data_path, crr_mtx_fname))
    num_docs = len(dense_crr_mtx)
    crr_mtx = sparse.csc_matrix(dense_crr_mtx)
    
    rated_movies = {1: 5, 2: 3, 3: 2}
    
    result_vec = random_walk(crr_mtx, num_docs, alpha, threshold, rated_movies.keys(), rated_movies.values())
    
    topk_ids = heapq.nlargest(k, range(len(result_vec)), result_vec.__getitem__)

    with open(os.path.join(data_path, moviefname)) as data_file:
        data = json.load(data_file)
        for id in topk_ids:
            temp_dict = data[id]
            movie_id = str(id)
            movie_name = temp_dict["name"]
            movie_description = temp_dict["description"]
            movie_image = temp_dict["url_image"]
            movie_url = temp_dict["url_web"]
            print '%s@%s@%s@%s@%s' % (movie_id, movie_name, movie_description, movie_image, movie_url)
"""            

    


movie_ids = [500]
p = np.zeros((num_docs, 1))
val = 1.0 / len(movie_ids)
for movie_id in movie_ids:
    p[movie_id] = val
#p = np.random.rand(num_docs, 1)
result_vec = random_walk(crr_mtx, num_docs, p, alpha, threshold)
for movie_id in movie_ids:
    result_vec[movie_id] = 0
print sum(result_vec)
topk_ids = heapq.nlargest(10, range(len(result_vec)), result_vec.__getitem__)

with open(os.path.join(data_path, moviefname)) as data_file:
        data = json.load(data_file)
        print(data[movie_id]["name"])
        print("Recommendations:")
        for id in topk_ids:
            print("%s %f" % (data[id]["name"], result_vec[id]))"""



