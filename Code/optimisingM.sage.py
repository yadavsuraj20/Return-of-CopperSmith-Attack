
# This file was *autogenerated* from the file optimisingM.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_1428 = Integer(1428); _sage_const_71 = Integer(71); _sage_const_4 = Integer(4); _sage_const_65537 = Integer(65537); _sage_const_256 = Integer(256); _sage_const_1024 = Integer(1024); _sage_const_512 = Integer(512); _sage_const_39 = Integer(39); _sage_const_0 = Integer(0); _sage_const_225 = Integer(225); _sage_const_126 = Integer(126); _sage_const_20 = Integer(20); _sage_const_2048 = Integer(2048)
from sage.doctest.util import Timer
from sage.functions.log import logb

prime_list = list(i for i in range(_sage_const_2 ,_sage_const_1428 ) if is_prime(i))

def primorial(n):
    x = _sage_const_1 
    for i in range(n):
        x *= prime_list[i]
    return x

# Algorithm 2 // Section 2.7
def optimisedM(M,order):
  newM = M
  for i in factor(M):
    g1 = Mod(g,Pi)
    ordpi = g.multiplicative_order()
    if((order % ordpi) != _sage_const_0 ):
      newM = newM/pi
  return newM


sizeofN = input('Size of N(256,512,1024,2048,4096) : ')
if(sizeofN==_sage_const_256 ):
  num = _sage_const_20 
elif(sizeofN==_sage_const_512 ):
  num = _sage_const_39 
elif(sizeofN==_sage_const_1024 ):
  num =_sage_const_71 
elif(sizeofN==_sage_const_2048 ):
  num = _sage_const_126 
else:
  num = _sage_const_225 

M = primorial(num)

g = Mod(_sage_const_65537 ,M)
order = g.multiplicative_order()
ord_factors = dict(factor(order))
fact_reversed = list(reversed(sorted(ord_factors.keys())))

newM = M

while(newM>_sage_const_2 **(sizeofN/_sage_const_4 )):
  ord_factors = dict(factor(order))
  fact_reversed = list(reversed(sorted(ord_factors.keys())))
  max_cost = _sage_const_0 ; value_of_i = _sage_const_0 ; actual_max_cost = _sage_const_1 
  for i in fact_reversed:
    for k in range(_sage_const_1 ,_sage_const_2 ):
      ord1 = order/(i**k)
      cost = _sage_const_1  ; actual_cost = _sage_const_1 
      for j in factor(M):
        g1 = Mod(_sage_const_65537 ,j[_sage_const_0 ])
        if((g1.multiplicative_order()%(i**k))==_sage_const_0 ):
          cost *= j[_sage_const_0 ]
          actual_cost *= j[_sage_const_0 ]
      cost = float(RDF(logb(i**k,cost)))
      if(cost>max_cost):
        max_cost = cost
        actual_max_cost = actual_cost
        value_of_i = i**k
  print(value_of_i)
  newM = newM/actual_max_cost
  order = order/value_of_i
  if(logb(newM,_sage_const_2 ) < sizeofN/_sage_const_4 ):
    newM = newM*actual_max_cost
    order = order*value_of_i
    break

print 'M : ',M,factor(M)
g = Mod(_sage_const_65537 ,M)
print 'ord : ',g.multiplicative_order(),factor(g.multiplicative_order())
print "M' : ",newM,factor(newM)
g = Mod(_sage_const_65537 ,newM)
print "ord' : ",g.multiplicative_order(),factor(g.multiplicative_order())
print "Size of M'",RDF(logb(newM,_sage_const_2 ))

