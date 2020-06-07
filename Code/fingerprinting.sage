prime_list = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167]
def primorial(n):
    x = 1
    for i in range(n):
        x *= prime_list[i]
    return x

def chinese_remainder(pairs,M): # Mi = M/pi^ei , Mi*yi = 1 mod pi^ei , X = xi*Mi*yi , M is order
    X = 0
    for piei in pairs:
        xi = pairs[piei]
        Mi = (M // piei)
        for j in range(piei):
            if((Mi*j)%piei == 1):
                yi = j
                break
        X += xi*Mi*yi
        X = X % M
    return X

pairs={}
def discrete_log(n,g,order,factors_of_order,m):
    for i in factors_of_order:
        piei = i**factors_of_order[i]
        gi = pow(g,order//piei,m)
        ni = pow(n,order//piei,m)
        xi = -1
        for j in range(0,piei):
            if pow(gi,j,m) == ni:
                xi = j
                pairs[piei]=xi
        if(xi==-1):
            return None
    return chinese_remainder(pairs,order)

m = primorial(39)
g = Mod(65537,m)
g_order = g.multiplicative_order()
factors_of_order = dict(factor(g_order))
data = input("N : ")
d = discrete_log(data, g, g_order, factors_of_order, m)
print "Value of c :",d