from sage.doctest.util import Timer

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

prime_list = list(i for i in range(2,1428) if is_prime(i))

def primorial(n):
    x = 1
    for i in range(n):
        x *= prime_list[i]
    return x

L = primorial(num)

g = Mod(65537,L)

power = sizeofN//2 -2

pmin = 3*2**power
pmax = 4*2**power

t.start()
x = 10000
# x = 50
u = lift(g^x)
while True:
  p = u + randrange(ceil(pmin/L),floor(pmax/L)) * L
  if p.is_prime(): print 'p',p ;break

t.start()
u = lift(g^randrange(L))
while True:
  q = u + randrange(ceil(pmin/L),floor(pmax/L)) * L
  if q.is_prime(): print 'q',q ;break

N = p*q
print 'N : ',N