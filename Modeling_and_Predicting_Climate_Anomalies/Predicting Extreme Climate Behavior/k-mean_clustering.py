sample = [(2,5), (1,4), (2,4), (2,3), (4,3), (5,3), (3,2), (4,2)]
objective_func = 0
clusterA = []
clusterB = []
a1, a2, b1, b2 = 0, 0, 0, 0

for point in sample:
    euc_distA = ((point[0]-1)**2 + (point[1]-4)**2)**(1/2)
    euc_distB = ((point[0]-5)**2 + (point[1]-3)**2)**(1/2)
    if euc_distA < euc_distB:
        clusterA.append(point)
        a1 += point[0]
        a2 += point[1]
        objective_func += euc_distA**2
    else:
        clusterB.append(point)
        b1 += point[0]
        b2 += point[1]
        objective_func += euc_distB**2

a1 /= len(clusterA)
a2 /= len(clusterA)

b1 /= len(clusterB)
b2 /= len(clusterB)
print(f"New Centroid A: ({a1}, {a2})\nNew Centroid B: ({b1}, {b2})")
print(f"Objective Function = {objective_func}")

########################################################################
new_set = [(5,8), (2,4), (0,0), (5,6), (3,3), (2,1), (9,8), (3,6), (5,1), (9,3)]
cluster_centroids = {1: (0,0), 2: (3,3), 3: (9,8)}

def assignItems(point_list, centroid_dict):
    assignments = {} # dictionary with points as keys and values are cluster numbers
    for point in point_list:
        p1, p2 = point
        min_euc_dist = float('inf')
        assignment = None
        for cluster, centroid in centroid_dict.items():
            c1, c2 = centroid
            curr_euc_dist = ((p1-c1)**2 + (p2-c2)**2)**(1/2)
            if curr_euc_dist < min_euc_dist:
                min_euc_dist = curr_euc_dist
                assignment = cluster
        assignments[point] = assignment
    return assignments

def findNewCentroids(assign_dict):
    x1sum, y1sum, x2sum, y2sum, x3sum, y3sum = 0, 0, 0, 0, 0, 0
    length1, length2, length3 = 0, 0, 0
    for point, cluster_assigned in assign_dict.items():
        px, py = point
        if cluster_assigned == 1:
            x1sum += px
            y1sum += py
            length1 += 1
        elif cluster_assigned == 2:
            x2sum += px
            y2sum += py
            length2 += 1
        else:
            x3sum += px
            y3sum += py
            length3 += 1
    cluster_dict = {}
    cluster_dict[1] = (x1sum/length1, y1sum/length1)
    cluster_dict[2] = (x2sum/length2, y2sum/length2)
    cluster_dict[3] = (x3sum/length3, y3sum/length3)
    return cluster_dict

def calculateJ(assign_dict, cluster_dict):
    J = 0
    for point, cluster_assigned in assign_dict.items():
        px, py = point
        cx, cy = cluster_dict[cluster_assigned]
        euc_dist = (px - cx)**2 + (py - cy)**2
        J += euc_dist
    return J

oldJ = float('-inf')
newJ = float('inf')
while oldJ != newJ:
    assignments = assignItems(new_set, cluster_centroids)
    cluster_centroids = findNewCentroids(assignments)
    oldJ = newJ
    newJ = calculateJ(assignments, cluster_centroids)
print(cluster_centroids)
print(assignments)