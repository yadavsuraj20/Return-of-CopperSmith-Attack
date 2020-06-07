from sage.doctest.util import Timer

prime_list = list(i for i in range(2,1428) if is_prime(i)) # list of prime numbers

def primorial(n): # calculating primorial
    x = 1
    for i in range(n):
        x *= prime_list[i]
    return x

t = Timer()

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

L = primorial(num)

g = Mod(65537,L)
print(g.multiplicative_order())

smooth = 2^7*3^3*5^2*7*11*13*17*19*23
print 'smooth',smooth
def smoothorder(l):
  return smooth % Mod(g,l).multiplicative_order() == 0
v = prod(l for l,e in factor(L) if smoothorder(l))
print "Value of M' : ",v

n = input('N : ')
print "M' : ",v
u = input("p mod M' : ")
g = Mod(g,v)
order2 = g.multiplicative_order()
print 'Order : ',order2, factor(order2)

t.start()

power = sizeofN//2 - 3
H = 10 + 2**(power) // v
u += floor((7*2**(power)) // v) * v

w = lift(1/Mod(v,n))

R.<x> = QQ[]
f = (w*u+H*x)/n
g = H*x
k = 3
m = 7
print 'multiplicity',k
print 'lattice rank',m

basis = [f^j for j in range(0,k)] + [f^k*g^j for j in range(m-k)]
basis = [b*n^k for b in basis]
basis = [b.change_ring(ZZ) for b in basis]

M = matrix(m)
for i in range(m):
  M[i] = basis[i].coefficients(sparse=False) + [0]*(m-1-i)

M = M.LLL()

Q = sum(z*(x/H)^i for i,z in enumerate(M[0]))

for r,multiplicity in Q.roots():
  print 'root found : ',r
  if u+v*r > 0:
    g = gcd(n,u+v*r)
    if g > 1:
      print 'successful factorization : ',[g,n/g]
print 'time taken by coppersmith : ',t.stop().cputime