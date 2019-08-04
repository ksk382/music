# -*- coding: utf-8 -*-

a = [i for i in range(0,300)]
print (a)

b = []

while len(a) > 0:
    for j in a[:99]:
        b.append(j)
    print (b)
    a = [i for i in a if i not in b]
    print (a)
    print (len(b), len(a))
    input('enter')
