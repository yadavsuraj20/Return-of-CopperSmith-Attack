
from sage.doctest.util import Timer
from sage.functions.log import logb

prime_list = list(i for i in range(2,1428) if is_prime(i))

def primorial(n):
    x = 1
    for i in range(n):
        x *= prime_list[i]
    return x

# Algorithm 2 // Section 2.7
def optimisedM(M,order):
  newM = M
  for i in factor(M):
    g1 = Mod(g,Pi)
    ordpi = g.multiplicative_order()
    if((order % ordpi) != 0):
      newM = newM/pi
  return newM


sizeofN = input('Size of N(256,512,1024,2048,4096) : ')
if(sizeofN==256):
  num = 20
elif(sizeofN==512):
  num = 39
elif(sizeofN==1024):
  num =71
elif(sizeofN==2048):
  num = 126
else:
  num = 225

M = primorial(num)

g = Mod(65537,M)
order = g.multiplicative_order()
ord_factors = dict(factor(order))
fact_reversed = list(reversed(sorted(ord_factors.keys())))

newM = M

while(newM>2**(sizeofN/4)):
  ord_factors = dict(factor(order))
  fact_reversed = list(reversed(sorted(ord_factors.keys())))
  max_cost = 0; value_of_i = 0; actual_max_cost = 1
  for i in fact_reversed:
    for k in range(1,2):
      ord1 = order/(i**k)
      cost = 1 ; actual_cost = 1
      for j in factor(M):
        g1 = Mod(65537,j[0])
        if((g1.multiplicative_order()%(i**k))==0):
          cost *= j[0]
          actual_cost *= j[0]
      cost = float(RDF(logb(i**k,cost)))
      if(cost>max_cost):
        max_cost = cost
        actual_max_cost = actual_cost
        value_of_i = i**k
  print(value_of_i)
  newM = newM/actual_max_cost
  order = order/value_of_i
  if(logb(newM,2) < sizeofN/4):
    newM = newM*actual_max_cost
    order = order*value_of_i
    break

print 'M : ',M,factor(M)
g = Mod(65537,M)
print 'ord : ',g.multiplicative_order(),factor(g.multiplicative_order())
print "M' : ",newM,factor(newM)
g = Mod(65537,newM)
print "ord' : ",g.multiplicative_order(),factor(g.multiplicative_order())
print "Size of M'",RDF(logb(newM,2))