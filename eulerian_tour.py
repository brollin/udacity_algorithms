# Eulerian Tour
#
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]

def connected_nodes(node, graph):
    connections = []
    for edge in graph:
        if edge[0] == node:
            connections.append(edge[1])
        elif edge[1] == node:
            connections.append(edge[0])
    return list(set(connections))

def get_degree(node, graph):
    degree = 0
    for edge in graph:
        if edge[0] == node or edge[1] == node:
            degree += 1

    return degree

def get_nodes(graph):
    nodes = []
    for edge in graph:
        for node in edge:
            nodes.append(node)

    return list(set(nodes))

def get_degrees(graph):
    nodes = get_nodes(graph)
    degrees = []
    for node in nodes:
        degrees.append(get_degree(node, graph))

    return degrees

def find_eulerian_tour(graph):
    
    # Check if all nodes have even degree, a prerequisite
    #   for the graph to have an Eulerian path
    # Also calculate the total number of visits required based on the degrees
    degrees = get_degrees(graph)
    visits_req = 0
    for degree in degrees:
        assert degree % 2 is 0, "Eulerian tour not possible with this graph"
        visits_req += degree
    visits_req /= 2

    # Capture all of the nodes of the graph
    nodes = get_nodes(graph)

    # Make an initial cycle
    tour = [graph[0][0], graph[0][1]]
    segments = [set([tour[0], tour[1]])]
    while tour[-1] is not tour[0]:
        for node in connected_nodes(tour[-1], graph):
            if node is not tour[-2]:
                segment = set([tour[-1], node])
                if segment not in segments:
                    segments.append(segment)
                    tour.append(node)
                    break
    
    # Find unvisited nodes
    unvisited = list(set(nodes) - set(tour))
   
    # Create cycles with unvisited nodes until all nodes have been visited
    while unvisited:

        # Find a node in the tour with adjacent unvisited nodes
        cycle = []
        cycle_started = False
        for node in tour:
            for con_node in connected_nodes(node, graph):
                if con_node in unvisited:
                    cycle = [node,con_node]
                    segments.append(set(cycle))
                    cycle_started = True
                    break
            if cycle_started:
                break

        # Complete the cycle
        while cycle[-1] is not cycle[0]:
            for node in connected_nodes(cycle[-1], graph):
                if node is not cycle[-2]:
                    segment = set([cycle[-1], node])
                    if segment not in segments:
                        segments.append(segment)
                        cycle.append(node)
                        break

        # Add cycle to tour
        slice_index = tour.index(cycle[0])
        del tour[slice_index]
        tour[slice_index:slice_index] = cycle

        # Find unvisited nodes
        unvisited = list(set(nodes) - set(tour))
   
    return tour

def test():
    #print find_eulerian_tour([(1, 2), (2, 3), (3, 1)])
    #print find_eulerian_tour([(1,2), (2,3),(3,4),(4,2),(2,5),(3,5),(1,3)])
    print find_eulerian_tour([(1,2),(1,9),(2,9),(3,2),(3,4),(2,4),(5,4),(5,10),(4,10),(6,10),(6,7),(7,10),(8,7),(8,9),(7,9)])

test()
