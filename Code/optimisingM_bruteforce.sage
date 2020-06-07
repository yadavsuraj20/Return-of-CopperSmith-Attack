from sage.functions.log import logb

prime_list = list(i for i in range(2,168) if is_prime(i))
print(prime_list)

def primorial(n):
    x = 1
    for i in range(n):
        x *= prime_list[i]
    return x

M = primorial(39)
g = Mod(65537,M)
order = g.multiplicative_order()
print order

factors = dict(factor(order))
print(factors)
candidates = set()
for i in factors:
    for j in range(1,factors[i]+1):
        candidates.add(i**j)
print candidates

def maxM(ordNew):
    newM = M
    for p in factor(M):
        g1 = Mod(65537,p[0])
        ordpi = g1.multiplicative_order()
        if(ordNew%ordpi!=0):
            newM = newM/p[0]
    return newM

S = Subsets(candidates)
# print(RDF(logb(len(S),2)))
best_order = order
best_M = M

for s in S.list():
    if(len(s)==0):
        continue
    order1 = prod(s)
    Mprime = maxM(order1)
    if(Mprime > 2**145):
        if(order1 < best_order):
            best_order = order1
            best_M = Mprime

print(best_order,best_M)
print(RDF(logb(best_M,2)))