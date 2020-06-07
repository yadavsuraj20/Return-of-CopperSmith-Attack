#Authors: Daniel J. Bernstein and Tanja Lange
#Origin:
from sage.doctest.util import Timer

prime_list = list(i for i in range(2,1428) if is_prime(i))

def primorial(n):
    x = 1
    for i in range(n):
        x *= prime_list[i]
    return x

t = Timer()

sizeofN = input('Size of N(256,512,1024,2048,4096) : ')
if(sizeofN==256):
  num = 20
  v = 3796316434940014295310
elif(sizeofN==512):
  num = 39
  v = 45092197507717713174331239195330276496994910
elif(sizeofN==1024):
  num =71
  v = 3377766159977061826604703412833277001367257204956613218025881383243158411145143430
elif(sizeofN==2048):
  num = 126
  v = 144232789069271883512611713774877402831210570440566770441755650506648048135262107760386369028414537535982562955069908031252963329370791390046449140798939859996010
else:
  num = 225
  v = 226740417611888036820712213674324302174869885035028963115201784550790316778187125705786574093030940610149506493790642121670630108816163569275478310828108699220477865957823010820958169655242202846457652454315163672455836480301324021058409409361410899209758268076987842949337435817645545149159592629869912899446243919930

L = primorial(num)
g = Mod(65537,L)

print "Value of M' : ",v

n = raw_input('N : ')
n = int(n)
g = Mod(g,v)
order2 = g.multiplicative_order()
print 'Order : ',order2
order2 = order2/10000

for i in range(10001):
    found = False
    for j in range(i*order2,(i+1)*order2):
        t.start()
        u = lift(g^j)
        power = sizeofN//2 - 3
        H = 10 + 2**(power) // v
        u += floor((7*2**(power)) // v) * v

        w = lift(1/Mod(v,n))

        R.<x> = QQ[]
        f = (w*u+H*x)/n
        g1 = H*x
        k = 3
        m = 7
        # print 'multiplicity', 3
        # print 'lattice rank', 7

        basis = [f^j for j in range(0,k)] + [f^k*g1^j for j in range(m-k)]
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
                g1 = gcd(n,u+v*r)
                if g1 > 1: print 'successful factorization',[g1,n/g1]; found = True; break
        if(found):
            break

    if(found):
      break