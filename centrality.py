# centrality.py

import csv
import pprint
import operator

def centrality(G, v):
    distance_from_start = {}
    open_list = [v]
    distance_from_start[v] = 0
    while len(open_list) > 0:
        current = open_list[0]
        del open_list[0]
        for neighbor in G[current].keys():
            if neighbor not in distance_from_start:
                distance_from_start[neighbor] = distance_from_start[current] + 1
                open_list.append(neighbor)
    return float(sum(distance_from_start.values()))/len(distance_from_start)

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def read_graph(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    actors = {}
    for (actor, movie, year) in tsv:
        make_link(G, actor, ' '.join([movie, year]))
        actors[actor] = 0
    return actors, G

(actors, G) = read_graph('imdb-1.tsv')

for actor in actors.keys():
    actors[actor] = centrality(G, actor)

actor_centrality = sorted(actors.items(), key=operator.itemgetter(1), reverse=True)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint( zip(range(25), actor_centrality[0:25]) )


