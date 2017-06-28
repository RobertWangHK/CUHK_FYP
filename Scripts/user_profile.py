import json
import numpy as np
from operator import add


def update_user_profile(movie_id, rating_result, movie_profile_dict, user_profile=None):
    num_features = 16529
    if not user_profile:
        user_profile = [0] * num_features
    if str(movie_id) not in movie_profile_dict:
        return user_profile
    movie_profile = movie_profile_dict[str(movie_id)]
    user_profile = list(map(add, user_profile, map(lambda x: x * rating_result, movie_profile)))
    return user_profile

def get_user_profiles_from_movies(user_ratings_matrix, movie_profile_fname, user_profile_fname):
    num_features = 16529
    with open(movie_profile_fname, "r") as input:
        movie_tags_dict = json.load(input)
    user_tags_dict = {}
    for i, line in enumerate(user_ratings_matrix):
        if i % 1000 == 0:
            print i
        line = line.split("\t")
        user_id = int(line[0])
        movie_id = int(line[1])
        rating_result = float(line[2]) - 2.5
        if user_id not in user_tags_dict:
            user_tags_dict[user_id] = [0] * num_features
        user_tags_dict[user_id] =update_user_profile(movie_id, rating_result, movie_tags_dict, user_tags_dict[user_id])
        """
        try:
            tags_list = movie_tags_dict[str(movie_id)]
            user_tags_dict[user_id] = list(map(add, user_tags_dict[user_id], map(lambda x: x * rating_result, tags_list)))

        except Exception as e:
            continue
        """
    with open(user_profile_fname, "w") as output:
        json.dump(user_tags_dict, output)
    return user_tags_dict  

if __name__ == '__main__':
    with open("data/user_ratedmovies.dat") as input:
        user_ratings = input.read().splitlines()
        del user_ratings[0]

    get_user_profiles_from_movies(user_ratings, "data/movie_explicit_tags", "data/user_explicit_tags")
    get_user_profiles_from_movies(user_ratings, "data/movie_implicit_tags", "data/user_implicit_tags")

"""
with open("data/movie_implicit_tags", "r") as input2:
    movie_implicit_tags_dict = json.load(input2)
input2.close()

#load movie explicit and implicit files
with open("data/movie_explicit_tags", "r") as input1:
    movie_explicit_tags_dict = json.load(input1)
num_features = len(movie_implicit_tags_dict[movie_implicit_tags_dict.keys()[0]])
print num_features
#user rating database -> user_id, movie_id, rating


#operate on user tags -> {user_id:{feature:score}}
#user_explicit_tags_dict = {}
user_implicit_tags_dict = {}

#index = 0

for line in user_ratings:
    line = line.split("\t")
    user_id = int(line[0])
    movie_id = int(line[1])
    rating_result = float(line[2]) - 2.5

    #if user_id not in user_explicit_tags_dict:
    #    user_explicit_tags_dict[user_id] = [0] * num_features
    if user_id not in user_implicit_tags_dict:
        user_implicit_tags_dict[user_id] = [0] * num_features
    try:
        #print "%s" % len(user_explicit_tags_dict)
        #generate user features list
        
        #explicit_tags_list = movie_explicit_tags_dict[str(movie_id)]
        
        implicit_tags_list = movie_implicit_tags_dict[str(movie_id)]
        #user_explicit_tags_dict[user_id] = list(map(add, user_explicit_tags_dict[user_id], map(lambda x: x * rating_result, explicit_tags_list)))
        #list(map(lambda x: x * rating_result, explicit_tags_list))
        
        user_implicit_tags_dict[user_id] = list(map(lambda x: x * rating_result, implicit_tags_list))
        
    
        
        
        #user_explicit_tags_dict[user_id][float(rating_result)].extend(explicit_tags_list)
        #user_implicit_tags_dict[user_id][float(rating_result)].extend(implicit_tags_list)

    except Exception as e:
        #print "exception: %s" % str(e)
        continue

#with open("data/user_explicit_tags", "w") as output1:
#    json.dump(user_explicit_tags_dict, output1)
#output1.close()

with open("data/user_implicit_tags", "w") as output2:
    json.dump(user_implicit_tags_dict, output2)
#output2.close()
"""