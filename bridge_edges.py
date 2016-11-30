# Bridge Edges v4
#
# Find the bridge edges in a graph given the
# algorithm in lecture.
# Complete the intermediate steps
#  - create_rooted_spanning_tree
#  - post_order
#  - number_of_descendants
#  - lowest_post_order
#  - highest_post_order
#
# And then combine them together in
# `bridge_edges`

# So far, we've represented graphs 
# as a dictionary where G[n1][n2] == 1
# meant there was an edge between n1 and n2
# 
# In order to represent a spanning tree
# we need to create two classes of edges
# we'll refer to them as "green" and "red"
# for the green and red edges as specified in lecture
#
# So, for example, the graph given in lecture
# G = {'a': {'c': 1, 'b': 1}, 
#      'b': {'a': 1, 'd': 1}, 
#      'c': {'a': 1, 'd': 1}, 
#      'd': {'c': 1, 'b': 1, 'e': 1}, 
#      'e': {'d': 1, 'g': 1, 'f': 1}, 
#      'f': {'e': 1, 'g': 1},
#      'g': {'e': 1, 'f': 1} 
#      }
# would be written as a spanning tree
# S = {'a': {'c': 'green', 'b': 'green'}, 
#      'b': {'a': 'green', 'd': 'red'}, 
#      'c': {'a': 'green', 'd': 'green'}, 
#      'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
#      'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
#      'f': {'e': 'green', 'g': 'red'},
#      'g': {'e': 'green', 'f': 'red'} 
#      }
#       
def create_rooted_spanning_tree(G, root):
    S = {}
    open_list = [root]
    while open_list:
        node = open_list.pop()
        for neighbor in G[node]:
            # If the nodes and edges already exist in the graph, skip the next steps
            if node in S and neighbor in S:
                if neighbor in S[node] and node in S[neighbor]:
                    continue
           
            # Check if the edge should be green (tree) or red (tree spanning)
            if node not in S or neighbor not in S:
                make_link(S, node, neighbor, 'green')
                open_list.append(neighbor)
            elif node not in S[neighbor] or neighbor not in S[node]:
                make_link(S, node, neighbor, 'red')
                
    return S

def make_link(S, n1, n2, color):
    if n1 not in S:
        S[n1] = {}
    if n2 not in S:
        S[n2] = {}
    (S[n1])[n2] = color
    (S[n2])[n1] = color

# This is just one possible solution
# There are other ways to create a 
# spanning tree, and the grader will
# accept any valid result
# feel free to edit the test to
# match the solution your program produces
def test_create_rooted_spanning_tree():
    G = {'a': {'c': 1, 'b': 1}, 
         'b': {'a': 1, 'd': 1}, 
         'c': {'a': 1, 'd': 1}, 
         'd': {'c': 1, 'b': 1, 'e': 1}, 
         'e': {'d': 1, 'g': 1, 'f': 1}, 
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1} 
         }
    S = create_rooted_spanning_tree(G, "a")
    assert S == {'a': {'c': 'green', 'b': 'green'}, 
                 'b': {'a': 'green', 'd': 'green'}, 
                 'c': {'a': 'green', 'd': 'red'}, 
                 'd': {'c': 'red', 'b': 'green', 'e': 'green'}, 
                 'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
                 'f': {'e': 'green', 'g': 'red'},
                 'g': {'e': 'green', 'f': 'red'} 
                 }
###########

# Return mapping between nodes of S and the post-order value
#   of that node
def post_order(S, root):
    post_orders = {}
    open_list = [root]
    #print 'Adding to open list: ', open_list
    while open_list:
        node = open_list[-1]
        neighbors = get_green_neighbors(S, node)
        if all([(neighbor in post_orders or neighbor in open_list) for neighbor in neighbors]):
            #print 'All neighbors of ', node, 'are post_ordered or open'
            post_orders[node] = len(post_orders) + 1
            open_list.pop()
            #print 'Post ordering!', neighbor, post_orders[neighbor]
        else:
            for neighbor in neighbors:
                if neighbor not in open_list: #TODO might need an extra term here, per nd below
                    open_list.append(neighbor)
                    #print 'Adding to open list: ', open_list
                    neighbor_neighbors = get_green_neighbors(S, neighbor)
                    #print 'Neighbors of ', neighbor, 'are', neighbor_neighbors
                    if len(neighbor_neighbors) == 1 and neighbor_neighbors[0] == node:
                        post_orders[neighbor] = len(post_orders) + 1
                        open_list.pop()
                        #print 'Post ordering!', neighbor, post_orders[neighbor]
                    else:
                        break
            
    return post_orders

def get_green_neighbors(S, node):
    neighbors = [] 
    #print 'get_green_neighbors:', node
    for neighbor in S[node]:
        #print S[node]
        if S[node][neighbor] == 'green':
            neighbors.append(neighbor)
    return neighbors

# This is just one possible solution
# There are other ways to create a 
# spanning tree, and the grader will
# accept any valid result.
# feel free to edit the test to
# match the solution your program produces
def test_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'green'}, 
         'c': {'a': 'green', 'd': 'red'}, 
         'd': {'c': 'red', 'b': 'green', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    assert po == {'a':7, 'b':6, 'c':1, 'd':5, 'e':4, 'f':3, 'g':2}

##############

def number_of_descendants(S, root):
    # Return mapping between nodes of S and the number of descendants
    #   of that node
    nd = {}
    open_list = [root]
    #print 'open_list: ',open_list
    while open_list:
        node = open_list[-1]
        #print 'inspecting node:', node
        neighbors = get_green_neighbors(S, node)
        #print '   has neighbors', neighbors
        if all([(neighbor in nd or neighbor in open_list) for neighbor in neighbors]):
            nd[node] = 1
            for neighbor in neighbors:
                if neighbor in nd:
                    nd[node] += nd[neighbor]
            #print 'node',node,'has only marked children and open parents'
            #print 'node',node,'had ', nd[node], 'descendants'
            open_list.pop()
        else:
            for neighbor in neighbors:
                if neighbor not in open_list and neighbor not in nd:
                    open_list.append(neighbor)
                    #print 'open_list: ',open_list
                    neighbor_neighbors = get_green_neighbors(S, neighbor)
                    if len(neighbor_neighbors) == 1 and neighbor_neighbors[0] == node:
                        nd[neighbor] = 1
                        #print 'neighbor',neighbor, 'is the lowest child'
                        open_list.pop()
                    else:
                        break

    return nd            

def test_number_of_descendants():
    S =  {'a': {'c': 'green', 'b': 'green'}, 
          'b': {'a': 'green', 'd': 'red'}, 
          'c': {'a': 'green', 'd': 'green'}, 
          'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
          'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
          'f': {'e': 'green', 'g': 'red'},
          'g': {'e': 'green', 'f': 'red'} 
          }
    nd = number_of_descendants(S, 'a')
    assert nd == {'a':7, 'b':1, 'c':5, 'd':4, 'e':3, 'f':1, 'g':1}

###############

def lowest_post_order(S, root, po):
    # Return a mapping of the nodes in S
    #   to the lowest post order value
    #   below that node
    #   (and you're allowed to follow 1 red edge)
    lpo = {}
    


    return lpo

def test_lowest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    l = lowest_post_order(S, 'a', po)
    print l
    assert l == {'a':1, 'b':1, 'c':1, 'd':1, 'e':2, 'f':2, 'g':2}

test_lowest_post_order()

################

def highest_post_order(S, root, po):
    # return a mapping of the nodes in S
    # to the highest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    pass

def test_highest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    h = highest_post_order(S, 'a', po)
    assert h == {'a':7, 'b':5, 'c':6, 'd':5, 'e':4, 'f':3, 'g':3}
    
#################

def bridge_edges(G, root):
    # use the four functions above
    # and then determine which edges in G are bridge edges
    # return them as a list of tuples ie: [(n1, n2), (n4, n5)]
    pass

def test_bridge_edges():
    G = {'a': {'c': 1, 'b': 1}, 
         'b': {'a': 1, 'd': 1}, 
         'c': {'a': 1, 'd': 1}, 
         'd': {'c': 1, 'b': 1, 'e': 1}, 
         'e': {'d': 1, 'g': 1, 'f': 1}, 
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1} 
         }
    bridges = bridge_edges(G, 'a')
    assert bridges == [('d', 'e')]

