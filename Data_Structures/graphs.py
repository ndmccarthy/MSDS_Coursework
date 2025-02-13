'''
Graphs
Graphs display a binary relation over a finite set with nodes/vertices and edges.
They cannot have edges pointing to the node it is originating from (loop) or multiple edges between the same nodes.
They can either be directed or undirected and are often used for describing networks (social, servers), circuits, programs (control flow, data flow), and roads/addresses.
They are also used to solve traversal problems, identify cycles, ranking nodes, shortest path, flow graphs, etc.

Representations
Graphs can be represented by an adjacency matrix, in which both rows and columns represent existing nodes and edges are represented with 1s and 0s.
    These are preferred for more dense graphs (when E is closer to V^2), or if you need to identify edges between two vertices quickly.
    Memory = theta(V^2)
    If a matrix is representing an undirected graph, it is equal to its transpose.
Graphs can also be represented by an adjacency list which is an array that holds a list of neighbors in each spot for the corresponding node.
    Adjacency lists are better for representing more sparse graphs (when E < V^2 by a lot).
    Memory = theta(V+E)

Traversals
Breadth First Search is a traversal looking at what is discoverable one step from  previous vertices and uses a FIFO queue to track it.
Depth First Search is a traversal that goes as far as it can along one path before backtracking.

Edge Types
 - Back Edge: points to an ancestor (v.d < u.d < u.f < v.f)
 --- creates a cycle in the graph
 - Cross Edge: points to something already seen in tree ([u.d, u.f] is disjoint from [v.d, v.f])
 - Forward Edge: points to a descendant that is not a direct child (u.d < v.d < v.f < u.f)

Maximal Strongly Connected Components (MSCC)
 - SCC: a subset of vertices in which for all pairs of vertices, there exists a path from vi to vj and vice versa, which entirely lies in the subset
 - MSCC: an SCC where any other additions to it make it no longer an SCC
  -- the biggest possible set that is still an SCC
A graph may be partitioned into MSCCs such that all vertices are accounted for.
This can be visualized in an MSCC supergraph, which must be a directed acyclic graph.
'''
from Functions.helper_functions import replace_Nones
from disjointed_forests import DisjointForests
from Functions.sorting_functions import quickSort

def num_connected_components(graph): 
    # connected components refers to MSCCs
    # graph must be an Undirected Graph class

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

def find_all_nodes_in_cycle(graph): 
    # graph is an UndirectedGraph class
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

    
class DFSTimeCounter:
    # This is a useful data structure for implementing a counter that counts the time.
    def __init__(self):
        self.count = 0
    
    def reset(self):
        self.count = 0
    
    def increment(self):
        self.count = self.count + 1
        
    def get(self):
        return self.count 
    
class UndirectedGraph:
    def __init__(self, num_vertices):
        # self.vertices is the number of vertices
        self.vertices = num_vertices
        # Initialize a set for each existing vertex
        self.adj_list = [ set() for ii in range(self.vertices) ]
        
    def add_edge(self, ii, jj):
        assert 0 <= ii < self.vertices
        assert 0 <= jj < self.vertices
        assert ii != jj
        # Make sure to add edge from ii to jj
        self.adj_list[ii].add(jj)
        # Also add edge from j to i
        self.adj_list[jj].add(ii)
        
    def get_neighboring_vertices(self, ii):
        # get a set of all vertices that are neighbors of the vertex ii
        assert 0 <= ii < self.vertices
        return self.adj_list[ii]
    
    def dfs_visit(self, ii:int, dfs_timer:DFSTimeCounter, discovery_times:list, finish_times:list, dfs_tree_parents:list, dfs_back_edges:list):
        assert 0 <= ii < self.vertices
        assert discovery_times[ii] == None
        assert finish_times[ii] == None
        # record parent node
        parent_not_found = True
        earlier_nodes = discovery_times[:ii]
        if len(earlier_nodes) == 0:
            parent = None
            parent_not_found = False
        else:
            earlier_nodes = replace_Nones(earlier_nodes, positive=False)
        while parent_not_found:
            last_discovered = max(earlier_nodes)
            if last_discovered != float('-inf'):
                last_discovered_id = discovery_times.index(last_discovered)
                if finish_times[last_discovered_id] != None:
                    earlier_nodes[last_discovered_id] = float('-inf')
                else:
                    parent = last_discovered_id
                    parent_not_found = False
            else:
                parent = None
                parent_not_found = False
        dfs_tree_parents[ii] = parent
        # record discovery time and increment timer
        discovery_times[ii] = dfs_timer.get()
        dfs_timer.increment()
        # search through neighbors in a sorted manner
        neighbors = self.get_neighboring_vertices(ii)
        if len(neighbors) == 0:
            pass
        else:
            neighbors = sorted(neighbors)
            for neighbor in neighbors:
                # if a neighbor has already been discovered, then record that a backedge exists and continue looking for undiscovered neighbors
                neighbor_discovered = bool(discovery_times[neighbor] != None)
                if neighbor_discovered:
                    if finish_times[neighbor] == None:
                        dfs_back_edges.append((ii, neighbor))
                    continue
                else:
                   # if ii has a neighbor that has not been discovered, start dfs_visit on that node
                   self.dfs_visit(neighbor, dfs_timer, discovery_times, finish_times, dfs_tree_parents, dfs_back_edges)
        # if all neighbors have already been discovered, then record the finish time for ii and increment the counter.
        finish_times[ii] = dfs_timer.get()
        dfs_timer.increment()
        
    def dfs_traverse_graph(self):
        dfs_timer = DFSTimeCounter()
        discovery_times = [None]*self.vertices
        finish_times = [None]*self.vertices
        dfs_tree_parents = [None]*self.vertices
        dfs_back_edges = []
        for node in range(self.vertices):
            if discovery_times[node] == None:
                self.dfs_visit(node, dfs_timer, discovery_times, finish_times, dfs_tree_parents, dfs_back_edges)
        # Clean up the back edges so that if (ii,jj) is a back edge then jj cannot be ii's parent.
        non_trivial_back_edges = [(ii,jj) for (ii,jj) in dfs_back_edges if dfs_tree_parents[ii] != jj]
        return (dfs_tree_parents, non_trivial_back_edges, discovery_times, finish_times)

class WeightedUndirectedGraph:
    def __init__(self, num_vertices):
        assert num_vertices >= 1, 'You are creating an empty graph -- disallowed'
        self.vertices = num_vertices
        self.edges = []
        self.vertex_data = [None]*self.vertices
        
    def set_vertex_data(self, vertex, data):
        assert 0 <= vertex < self.vertices
        self.vertex_data[vertex] = data
        
    def get_vertex_data(self, vertex):
        assert 0 <= vertex < self.vertices
        return self.vertex_data[vertex] 
        
    def add_edge(self, node, vertex, weight):
        assert 0 <= node < self.vertices
        assert 0 <= vertex < self.vertices
        assert node != vertex
        # Make sure to add edge from node to vertex with weight
        self.edges.append((node, vertex, weight))
        
    def sort_edges(self):
        # sort edges in ascending order of weights
        self.edges = sorted(self.edges, key=lambda edg_data: edg_data[2])

def compute_scc(graph=WeightedUndirectedGraph, weight_cap):
    # finds MSCCs in a weighted graph using the properties of a Disjointed Forest
    # create a disjoint forest with as many elements as number of vertices
    num_vertices = graph.vertices
    forest = DisjointForests(num_vertices)
    # reconstruct trees
    for ii in range(num_vertices):
        forest.make_set(ii)
    weights = []
    graph_edges = []
    for edge in graph.edges:
        graph_edges.append(edge)
        node, vertex, weight = edge
        if weight <= weight_cap:
            weights.append(weight)
    quickSort(weights, 0, len(weights)-1)
    forest_edges = []
    for entry in weights:
        for edge in graph_edges:
            node, vertex, weight = edge
            edge_id = graph_edges.index(edge)
            if entry == weight:
                forest_edges.append((node, vertex))
                graph_edges.pop(edge_id)
    for edge in forest_edges:
        
        forest.union(edge)
    # Next compute the strongly connected components using the union find data structure
    # extract a set of sets from d
    return forest.dictionary_of_trees()