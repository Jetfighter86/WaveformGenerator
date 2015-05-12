__author__ = 'Phillip'

import decimal
A1=list()
B1=list()
C1=list()
for i in range(10):
    A1.append(i)
    B1.append(i)
for x,y, in zip(A1,B1):
    C1.append(x+y)

print C1