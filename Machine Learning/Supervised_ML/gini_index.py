# calculate Gini Index

cluster1 = [7, 2] # 7 blue, 2 red in cluster 1
cluster2 = [1, 6] # 1 blue, 6 red in cluster 2
classes = [cluster1, cluster2]

def gini_index(clusters):
    total_points = sum(sum(cluster) for cluster in clusters)
    gini = 0
    for cluster in clusters:
        num_in_cluster = sum(cluster)
        weight = num_in_cluster / total_points
        cluster_gini = 0
        for ii in range(len(cluster)):
            num_points = cluster[ii]
            prop_accurate = num_points / num_in_cluster
            cluster_gini += prop_accurate * (1 - prop_accurate)
        gini += weight * cluster_gini
    return gini


purity = gini_index(classes)
print(round(purity, 5))