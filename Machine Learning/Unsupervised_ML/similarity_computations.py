# Computing user similarity wuth different methods

import pandas as pd
import numpy as np

# upload data
games = ["WatchDog", "GTAV", "PUBG", "StarCraft", "CallofDuty", "FIFA", "WOW", "Minecraft"]
firechicken = [3, 3, 4, 0, 4, 2, 3, 0]
mike = [3, 5, 4, 3, 3, 0, 0, 4]
zeph = [0, 4, 0, 5, 0, 0, 2, 1]
dad =[2, 0, 0, 4, 0, 4, 4, 5]

utility_matrix = pd.DataFrame([firechicken, mike, zeph, dad], columns=games, index=["Firechicken", "Mike", "Zephyros", "Dadvador"])

# calculate jaccard similarity
def jaccard_similarity(a,b):
    return round((a*b).sum()/((a+b)>0).sum(), 3)

# calculate cosine similarity
def cosine_similarity(user1, user2):
    return round(np.dot(user1, user2)/(np.linalg.norm(user1)*np.linalg.norm(user2)), 3)

# convert ratings to binary (good/bad <- 1/0)
def binarize_ratings(util_mat):
    bin_um = util_mat.copy()
    def map_rating(x):
        if x >= 3:
            return 1
        else:
            return 0
    bin_um = bin_um.map(map_rating)
    return bin_um

def binarize_purchases(util_mat):
    bin_um = util_mat.copy()
    def map_purchase(x):
        if x == 0:
            return 0
        else:
            return 1
    bin_um = bin_um.map(map_purchase)
    return bin_um

def normalize_ratings(util_mat):
    norm_um = util_mat.copy()
    for user in norm_um.index:
        mean_rating = norm_um.loc[user].mean()
        norm_um.loc[user] = norm_um.loc[user] - mean_rating
    return norm_um

# test the functions
print(utility_matrix)

purchase_matrix = binarize_purchases(utility_matrix)
print("Purchase Matrix:")
print(purchase_matrix)
'''
norm_utility_matrix = normalize_ratings(utility_matrix)
print("Normalized Utility Matrix:")
print(norm_utility_matrix)
'''
binary_rating_matrix = binarize_ratings(utility_matrix)
print("Binarized Rating Matrix:")
print(binary_rating_matrix)

print("Jaccard Similarity between Mike and Zephyros:", jaccard_similarity(purchase_matrix.loc["Mike"], purchase_matrix.loc["Zephyros"]))
print("Cosine Similarity between Firechicken and Mike:", cosine_similarity(purchase_matrix.loc["Firechicken"], purchase_matrix.loc["Mike"]))
print("Jaccard Similarity between Firechicken and Zephyros:", jaccard_similarity(binary_rating_matrix.loc["Firechicken"], binary_rating_matrix.loc["Zephyros"]))