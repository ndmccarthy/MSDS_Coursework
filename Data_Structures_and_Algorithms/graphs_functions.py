# This file was created to shorten the length of the original file that held all graphs related items.

from graphs_classes import *
from disjointed_forests import DisjointForests
from heaps import PriorityQueue

def num_connected_components(graph=UndirectedGraph): 
    # connected components refers to MSCCs

    # created list of nodes in descending order of finish
    (dfs_tree_parents, non_trivial_back_edges, discovery_times, finish_times) = graph.dfs_traverse_graph()
    descend_finish = []
    while len(finish_times) > len(descend_finish):
        last_value = max(finish_times)
        last_finished = finish_times.index(last_value)
        descend_finish.append(last_finished)
        finish_times[last_finished] = float('-inf')

    # transposed graph is the same as original graph for undirected graphs; no need to transpose
    # complete DFS but remove nodes from descend_finish as they're visited
    # when the original node is returned to in that iteration, MSCC is complete
    num_nodes = graph.vertices
    timer = DFSTimeCounter()
    d_list = [None]*num_nodes
    f_list = [None]*num_nodes
    p_list = [None]*num_nodes
    backedges = []
    mscc_count = 0
    for node in descend_finish:
        graph.dfs_visit(node, timer, d_list, f_list, p_list, backedges)
        for time in d_list:
            if time != None:
                node_visited = d_list.index(time)
                visited_place = descend_finish.index(node_visited)
                if visited_place != node:
                    descend_finish.pop(visited_place)
                d_list[node_visited] = None
        mscc_count += 1
    return mscc_count

def find_all_nodes_in_cycle(graph=UndirectedGraph): 
    # returns a set of the nodes that exist in a cycle (may not be the same cycle)
    set_of_nodes = set()
    (parents, nontrivial_backedges, d_times, f_times) = graph.dfs_traverse_graph()
    print(f"Nontrivial Backedges: {nontrivial_backedges}")
    print(f"Parents List: {parents}")
    # if backedge exists, then a loop does
    for edge in nontrivial_backedges:
        # add nodes in backedge to set
        first_node, second_node = edge
        set_of_nodes.add(first_node)
        set_of_nodes.add(second_node)
        # look for parents
        first_parent = parents[first_node]
        second_parent = parents[second_node]
        edge_parents = [first_parent, second_parent]
        # add direct parents until loop is completed (parent is None)
        for parent in edge_parents:
            while parent is not None:
                set_of_nodes.add(parent)
                parent = parents[parent]
    return set_of_nodes

def create_forest(graph=WeightedUndirectedGraph):
    # helper function for compute_scc and compute_mst
    # create a disjointed forest with as many elements as number of vertices
    num_vertices = graph.vertices
    forest = DisjointForests(num_vertices)
    for ii in range(num_vertices):
        forest.make_set(ii)
    return forest

def compute_scc(weight_cap, graph=WeightedUndirectedGraph):
    # finds MSCCs in a weighted graph using the properties of a disjointed forest
    # this is essentially an implementation of Kruskal's Algorithm for finding Minimal Spanning Trees
    forest = create_forest(graph)
    # sort edges by weight and add as applicable
    graph.sort_edges()
    for edge in graph.edges:
        node, vertex, weight = edge
        # edges must have a weight <= weight_cap
        if weight <= weight_cap:
            # add edge to the forest if the node/vertex are not in the same tree
            if forest.find(node) != forest.find(vertex):
                forest.union(node, vertex)
    # extract the trees from forest
    return forest.dictionary_of_trees()

def compute_mst(graph=WeightedUndirectedGraph):
    # finds minimal spanning tree (MST) using Kruskal's Alg.
    # similar to compute_scc but does not have a weight_cap and returns list of edges (as tuples) followed by the weight of the entire MST
    # create disjointed forest
    forest = create_forest(graph)
    # sort edges by weight and add as applicable
    graph.sort_edges()
    # create MST
    mst_edges = []
    mst_weight = 0
    for edge in graph.edges:
        node, vertex, weight = edge
        # add edge to the forest if the node/vertex are not in the same tree
        if forest.find(node) != forest.find(vertex):
            forest.union(node, vertex)
            # add edges to list
            mst_edges.append(edge)
            # add edge weight to mst_weight
            mst_weight += weight
    return (mst_edges, mst_weight)

def computeShortestPath(graph=DirectedGraphFromImage, source_coordinates=tuple, dest_coordinates=tuple):
    # uses a variation of Dijkstra's alg to avoid computing all possibilities and return a list of vertices that make up the shortest path and its distance as a tuple
    q = PriorityQueue()
    (sx, sy) = source_coordinates
    source = graph.get_vertex_from_coords(sx, sy)
    source.d = 0
    q.insert(source)
    while q.is_empty == False:
        u = q.get_and_delete_min()
        u.processed = True
        if (u.x, u.y) == dest_coordinates:
            break
        neighbors = graph.get_list_of_neighbors(u)
        for v in neighbors:
            w = graph.getEdgeWeight(u,v)
            print(v.processed)
            print(v.d)
            print(u.d + w)
            if v.processed == False and v.d > u.d + w:
                v.d = u.d + w
                v.pi = u
                if v not in q.q:
                    q.insert(v)
                else:
                    q.update_vertex_weight(v)
    path = []
    (dx, dy) = dest_coordinates
    item = graph.get_vertex_from_coords(dx, dy)
    distance = item.d
    while item.pi != None:
        item_coords = (item.x, item.y)
        path.insert(0, item_coords)
        item = item.pi
    path.insert(0, source_coordinates)
    return (path, distance)