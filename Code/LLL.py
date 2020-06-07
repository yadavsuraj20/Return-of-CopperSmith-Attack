import numpy as np
from copy import deepcopy as dc
import math
def proj(vec1,vec2):
    # print(vec1)
    # print(vec2)
    norm2=math.sqrt(np.sum(np.power(vec2,2)))
    # print(norm2)
    projectionVal=np.dot(vec1,vec2)/norm2
    return vec2/norm2*projectionVal


def grahmschmidt(basis):
    ans=np.zeros(basis.shape)
    ans[0]=basis[0]
    # print(len(ans))
    for i in range(1,len(ans)):
        # basis_vector=np.zeros((1,basis.shape[1]))
        basis_vector=dc(basis[i])
        # print(basis_vector)
        for j in range(i):
            # print(j)
            basis_vector=basis_vector-proj(basis_vector,ans[j])
            # print(basis_vector)
        ans[i]=basis_vector
    return ans



def LLL_reduce(basis,delta):
    num_vecs=len(basis)
    ortho=grahmschmidt(basis)
    # print(ortho)
    # return
    def mu(i,j):
        # print(ortho[i],ortho[j])
        return np.dot(basis[i],ortho[j])/np.dot(ortho[j],ortho[j])
    k=1
    while k<num_vecs:
        for j in range(k-1,-1,-1):
            mukj=mu(k,j)
            if(abs(mukj)>0.5):
                basis[k]=basis[k]-basis[j]*round(mukj)
                ortho=grahmschmidt(basis)
        if(np.dot(ortho[k],ortho[k])>=(delta-mu(k,k-1)**2)*np.dot(ortho[k-1],ortho[k-1])):
            k=k+1
        else:
            bk1temp=dc(basis[k])
            bktemp=dc(basis[k-1])
            basis[k]=bktemp
            basis[k-1]=bk1temp
            ortho=grahmschmidt(basis)
            k=max(k-1,1)
    return basis
b=np.array([[1, 1, 1], [-1, 0, 2],[3,5,6]])
print(LLL_reduce(b,0.75))
#Referred https://github.com/orisano/olll for help