# finding the shortest path from A to B
# this particular implementation is a grid of width W and height H with circles that you cannot traverse on
# we are trying to get from (0,0) to (W,H)

from math import sqrt
from graphs_classes import Vertex
from heaps import PriorityQueue

# You may use this function to test if a point lies inside given circle.
def ptInCircle(x,y, circles_list):
    for (xc,yc,rc) in circles_list:
        d = sqrt ( (x-xc)**2 + (y-yc)**2)
        if d <= rc:
            return True
    return False

def getVerticesandEdges(width, height, forbidden_circles_list):
    # initialize dictionary of vertices; keys are coordinates as tuple
    vertices = {}
    for x_val in range(width + 1):
        for y_val in range(height + 1):
            node = Vertex(x_val, y_val)
            vertices[(x_val, y_val)] = node
    source = (0,0)
    vertices[source].d = 0
    # initialize edges list
    edges = []
    for node in vertices.keys():
        (x_val, y_val) = node
        neighbors = [(x_val + 1, y_val), (x_val, y_val + 1), (x_val - 1, y_val), (x_val, y_val - 1)]
        for neighbor in neighbors:
            x, y = neighbor
            if neighbor in vertices.keys(): # check if potential neighbor is actually a part of the coordinate system
                # only add edges that do not tough the forbidden circles
                if not ptInCircle(x, y, forbidden_circles_list):
                    edges.append((node, neighbor, 1))
    return(vertices, edges)

def getNeighbors(edges=list, node=Vertex):
    neighbors = []
    node_coords = (node.x, node.y)
    for edge in edges:
        if edge[0] == node_coords:
            neighbors.append((edge[1], edge[2]))
    return neighbors
    
def findPath(width, height, forbidden_circles_list):
    # width is a positive number
    # height is a positive number
    # forbidden_circles_list is a list of triples [(x1, y1, r1),..., (xk, yk, rk)]
    assert width >= 1
    assert height >= 1
    assert all(x <= width and x >=0 and y <= height and y >= 0 and r > 0 for (x,y,r) in forbidden_circles_list)
    # using the Dijkstra's algorithm
    # get vertices and edges
    vertices, edges = getVerticesandEdges(width, height, forbidden_circles_list)
    q = PriorityQueue()
    source_coordinates = (0,0)
    source  = vertices[(0,0)]
    q.insert(source)
    dest_coordinates = (width, height)
    while len(q.q) > 1:
        # stop loop if not possible to get answer
        u = q.get_and_delete_min()
        u.processed = True
        if (u.x, u.y) == dest_coordinates:
            break
        neighbors = getNeighbors(edges, u)
        for neighbor in neighbors:
            v_coords, w = neighbor
            v = vertices[v_coords]
            if v.processed == False and v.d > u.d + w:
                v.d = u.d + w
                v.pi = u
                if v not in q.q:
                    q.insert(v)
                else:
                    q.update_vertex_weight(v)
    path = []
    item = vertices[dest_coordinates]
    while item.pi != None:
        item_coords = (item.x, item.y)
        path.insert(0, item_coords)
        item = item.pi
    if len(path) != 0:
        path.insert(0, source_coordinates)
    return (path)