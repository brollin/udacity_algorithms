import csv
import pprint
import operator

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 0
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 0
    return G

def read_graph(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    chars = []
    books = []
    for (char, book) in tsv:
        make_link(G, char, book)
        if char not in chars: chars.append(char)
        if book not in books: books.append(book)
    return chars, books, G

(chars, books, marvelG) = read_graph('marvel.tsv')

chars = list(set(chars))
charG = {}
for char1 in chars:
    for book in marvelG[char1]:
        for char2 in marvelG[book]:
            if char1 > char2:
                 make_link(charG, char1, char2)

# Remove any chars that are not in the charG graph
chars = charG.keys()

# Go through each book and add a connection to the charG connection
# strength graph for each pair of characters
for book in books:
    chars_to_pair = marvelG[book].keys()
    for i, char1 in enumerate(chars_to_pair):
        if i < len(chars_to_pair) - 1:
            for j, char2 in enumerate(chars_to_pair[i+1:]):
                charG[char1][char2] += 1
                charG[char2][char1] += 1

# Capture strength of each connection in list:
captured_conns = {}
checked_chars = []
for char1 in charG:
    for char2 in charG[char1]:
        if char2 not in checked_chars:
            captured_conns[char1 + ' ' + char2] = charG[char1][char2]
    checked_chars.append(char1)

conn_weights = sorted(captured_conns.items(), key=operator.itemgetter(1), reverse=True)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint( zip(range(25), conn_weights[0:25]) )
import pdb
pdb.set_trace()

