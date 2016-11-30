
n = 256
p = .25
nodes = range(n)
edges = 0
for i in nodes:
    for j in nodes[(i+1):]:
        import random
        if random.random() >= .25:
            edges+=1
print edges
