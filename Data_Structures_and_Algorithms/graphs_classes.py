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

from helper_functions import replace_Nones
from special_application_functions import fixPixelValues


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

class Vertex: 
    # This is the outline for a vertex data structure that relies on (x, y) coordinates for it's keys
    # used in finding shortest path using Dijkstra's alg, but without calculating all possibilities

    def __init__ (self,  i, j):
        self.x = i # The x coordinate
        self.y = j  # The y coordinate
        self.d = float('inf') # the shortest path estimate
        self.processed = False # Has this vertex's final shortest path distance been computed
        # this is important for Dijksatra's algorithm
        # We will track where the vertex is in the priority queue.
        self.idx_in_priority_queue = -1 # The index of this vertex in the queue
        self.pi = None # the parent vertex in the shortest path tree.
        
    def reset(self):
        self.d = float('inf')
        self.processed = False # Has this vertex's final shortest path distance been computed
        # this is important for Dijksatra's algorithm
        # We will track where the vertex is in the priority queue.
        self.idx_in_priority_queue = -1 # The index of this vertex in the queue
        self.pi = None # the parent vertex in the shortest path tree.


class DirectedGraphFromImage:
    def __init__(self, img):
        self.img = img
        self.coords2vertex = {} # construct a dictionary that maps coordinates [(i,j)] to corresponding vertices in graph
        
    def get_vertex_from_coords(self, i, j):
        if (i,j) in self.coords2vertex: # is pixel (i,j) already there? 
            return self.coords2vertex[(i,j)] # if yes, just return the vertex corresponding
        v = Vertex(i, j)
        self.coords2vertex[(i,j)] = v
        return v
    
    def getEdgeWeight(self, u, v):
        # Given (x,y) coordinates of two neighboring pixels, calculate the edge weight.
         # We take the squared euclidean distance between the pixel values and add 0.1
        img = self.img
        # get edge weight for edge between u, v
        i0,j0 = u.x, u.y
        i1,j1 = v.x, v.y
        height, width, _ = img.shape
        # First make sure that the edge is legit
        # Edges can only go from each pixel to neighboring pixel
        assert i0 >= 0 and j0 >= 0 and i0 < width and j0 < height # pixel position valid?
        assert i1 >= 0 and j1 >= 0 and i1 < width and j1 < height # pixel position valid?
        assert -1 <= i0 - i1 <= 1 # edge between node and neighbor?
        assert -1 <= j0 - j1 <= 1
        px1 = fixPixelValues(img[j0,i0])
        px2 = fixPixelValues(img[j1,i1])
        return 0.1 + (px1[0] - px2[0])**2 + (px1[1] - px2[1])**2 + (px1[2]- px2[2])**2

    # Function: get_list_of_neighbors
    # Given a vertex in the graph, get its list of neighbors
    #  I.e, for given vertex `vert` return a list [(v1, w1), (v2, w2),..,(vk,wk)]
    #  Such that vert has an edge to v1 with weight w1, edge to v2 with weight w2 and ... 
    #   edge to vk with weight wk
    # Note that rather than build an adjacency list up front, we simply call this function
    # to get the neighbors of a vertex.
    def get_list_of_neighbors(self, vert):
        img = self.img
        i = vert.x
        j = vert.y
        height, width, _ = img.shape
        lst = []
        if i > 0:
             # Get the adjacent vertex directly to the WEST
            # What is the weight of the edge from pixel (i,j) to (i-1,j)
            v0 = self.get_vertex_from_coords(i-1, j)
            w0 = self.getEdgeWeight(vert, v0)
            # Append the adjacent vertex and its weight.
            lst.append((v0, w0))
        if j > 0:
            # Get the adjacent vertex directly to the SOUTH
            v1 = self.get_vertex_from_coords(i, j-1)
            w1 = self.getEdgeWeight(vert, v1)
            # Append the adjacent vertex and its weight.
            lst.append((v1, w1))    
        if i < width-1:
            # EAST
            v2 = self.get_vertex_from_coords(i+1, j)
            w2 = self.getEdgeWeight( vert, v2)
            lst.append((v2, w2))
        if j < height-1:
            # NORTH
            v3 = self.get_vertex_from_coords(i, j+1)
            w3 = self.getEdgeWeight(vert, v3)
            lst.append((v3, w3))
        return lst