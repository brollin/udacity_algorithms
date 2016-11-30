#
# Given a list of numbers, L, find a number, x, that
# minimizes the sum of the absolute value of the difference
# between each element in L and x: SUM_{i=0}^{n-1} |L[i] - x|
# 
# Your code should run in Theta(n) time
#

def partition(L, v):
    smaller = []
    bigger  = []
    for val in L:
        if val < v: smaller += [val]
        if val > v: bigger  += [val]
    return (smaller, [v], bigger)

def top_k(L, k):
    import random
    v = L[random.randrange(len(L))]
    (left, middle, right) = partition(L, v)
    if len(left) == k: return left
    if len(left)+1 == k: return left+[v]
    if len(left) > k: return top_k(left, k)
    return left+[v]+top_k(right, k-len(left)-1)

def minimize_absolute(L):
    x = 0

    x = top_k(L, len(L)/2 if len(L)%2==0 else len(L)/2+1)

    return max(x)



