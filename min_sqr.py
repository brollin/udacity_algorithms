#
# Given a list of numbers, L, find a number, x, that
# minimizes the sum of the square of the difference
# between each element in L and x: SUM_{i=0}^{n-1} (L[i] - x)^2
# 
# Your code should run in Theta(n) time
# 

def minimize_square(L):

    x = sum(L)/float(len(L))
    
    return x

import random
length = 20
a = [ random.random()*100 for b in range(length)  ]
print 'list:', a
print 'minimize_square:', 	minimize_square(a), 'yields', sum([ (i - minimize_square(a)) for i in a ])
print 'minimize_square-1:', minimize_square(a)-1, 'yields', sum([ (i - minimize_square(a)-1) for i in a ])
print 'minimize_square+1:', minimize_square(a)+1, 'yields', sum([ (i - minimize_square(a)+1) for i in a ])



