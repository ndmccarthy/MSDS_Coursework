import numpy as np

# K-Means Clustering
def k_means_clustering(centroids, dataset):

#   Description: Perform k means clustering for 2 iterations given as input the dataset and centroids.
#   Input:
#       1. centroids - A list of lists containing the initial centroids for each cluster. 
#       2. dataset - A list of lists denoting points in the space.
#   Output:
#       1. results - A dictionary where the key is iteration number and store the cluster assignments in the 
#           appropriate clusters. Also, update the centroids list after each iteration.
    
    # in this example, k = 3
    # initialize results dictionary
    result = {
        '1': { 'cluster1': [], 'cluster2': [], 'cluster3': [], 'centroids': []},
        '2': { 'cluster1': [], 'cluster2': [], 'cluster3': [], 'centroids': []}
    }
    # complete 2 iterations (for purpose of this exercise)
    for iteration in range(1, 3): # account for iteration count starting at 1, not 0; go up to 2
        iteration_key = str(iteration) # make iteration a string instead of a number (as set up)
        # assign each object to the nearest centroid
        # iterate through each object (type = list)
        for object in dataset:
            # calculate which centroid is closest (use pythagorean theorem)
            # iterate through centroids and store in list
            distances = []
            for centroid in centroids:
                dist = np.sqrt(((object[0]-centroid[0])**2)+((object[1]-centroid[1])**2))
                distances.append(dist)
            min_dist = min(distances)
            # update results with cluster assignment
            cluster_assignment = distances.index(min_dist) + 1 # account for cluster count starting at 1, not 0
            cluster_key = 'cluster' + str(cluster_assignment)
            result[iteration_key][cluster_key].append(object)
        # update centroids based on objects assigned to cluster
        # find mean of all objects in each cluster
        def x_y_means(cluster):
            Xs = [object[0] for object in cluster]
            Ys = [object[1] for object in cluster]
            x_mean = sum(Xs)/len(Xs)
            y_mean = sum(Ys)/len(Ys)
            return [x_mean, y_mean]
        # retrieve iteration clusters
        for ii in range(1, 4): # need clusters 1-3
            cluster_key = 'cluster' + str(ii)
            cluster = result[iteration_key][cluster_key]
            new_centroid = x_y_means(cluster)
            # update results with new centroids
            result[iteration_key]['centroids'].append(new_centroid)
        # update centroids list with new centroids
        centroids = result[iteration_key]['centroids']
    return result

#########################
#       TESTING
#########################

dataset = [[46, 33], [26, 21], [23, 96], [82, 20], [25, 42], [29, 99], [30, 64], [57, 51], [12, 68], [25, 9]]
centroids = [[12, 68], [46, 33], [25, 42]]
result_expected = {'1': {'cluster1': [[23, 96], [29, 99], [30, 64], [12, 68]],
                         'cluster2': [[46, 33], [82, 20], [57, 51], [25, 9]], 
                         'cluster3': [[26, 21], [25, 42]], 
                         'centroids': [[23.5, 81.75], [52.5, 28.25], [25.5, 31.5]]},
                    '2': {'cluster1': [[23, 96], [29, 99], [30, 64], [12, 68]], 
                          'cluster2': [[46, 33], [82, 20], [57, 51]], 
                          'cluster3': [[26, 21], [25, 42], [25, 9]], 
                          'centroids': [[23.5, 81.75], [61.666666666666664, 34.666666666666664], [25.333333333333332, 24.0]]}}

result = k_means_clustering(centroids,dataset)
assert(result == result_expected)

'''-----------------------------------------------------------------------------------------------------------'''

# EM Clustering

def em_clustering(centroids, dataset):

#   Input: 
#       1. centroids - A list of lists with each value representing the mean and standard deviation values picked from a gausian distribution.
#       2. dataset - A list of points randomly picked.
#   Output:
#       1. results - Return the updated centroids(updated mean and std values after the EM step) after the first iteration.

    # make dataset and centroids into arrays for vectorized calculations
    data = np.array(dataset) # (n,)
    data = data[:, None] # reshape to (n, 1)
    clusters = np.array(centroids) # (k, 2)
    means = clusters[:, 0] # (k,)
    sds = clusters[:, 1] # (k,)

    # calculate probability of each point belonging to a specific cluster (for all clusters)
    exponent = (-1/2) * ((data - means)/sds)**2
    point_probabilities = np.exp(exponent) / (sds * np.sqrt(2 * np.pi)) # (n, k)
    point_prob_normalizer = point_probabilities.sum(axis=1, keepdims = True) # (n, 1)
    cluster_membership = point_probabilities / point_prob_normalizer # (n, k)

    # calculate new means
    weighted_cluster_membership = data * cluster_membership # (n, k)
    weighted_cluster_membership_sums = weighted_cluster_membership.sum(axis=0) # (k,)
    cluster_membership_normalizer = cluster_membership.sum(axis=0) # (k,)
    new_means = weighted_cluster_membership_sums / cluster_membership_normalizer # (k,)

    # calculate new standard deviations (make sure to update point probabilities and cluster emembership)
    sd_numerator = ((data - new_means[None, :])**2) * cluster_membership # (n, k)
    sd_num_sum = sd_numerator.sum(axis=0) # (k,)
    new_sds = np.sqrt(sd_num_sum/cluster_membership_normalizer) # (k,)

    # get means and sds into correct format
    new_centroids = np.stack((new_means, new_sds), axis=-1)
    new_centroids = new_centroids.tolist()

    return new_centroids


################################
#       TESTING
################################

data = [8, 16, 13, 9, 18, 15, 7, 5, 7, 3]
EM_centroids = [[13, 2], [2, 16]]
new_centroids_expected = [[13.346550530668159, 3.236599802533008], [7.9971108077796735, 4.473417525043109]]
new_centroids = em_clustering(EM_centroids, data)
print(new_centroids)
assert(new_centroids == new_centroids_expected)