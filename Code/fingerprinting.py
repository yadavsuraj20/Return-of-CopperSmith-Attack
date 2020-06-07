import json
import argparse
import base64
import hashlib
import sys
import os
import re
import math
import datetime
from math import ceil, log

########################################################################################################
def pem_to_der(x):
    if x is None:
        return None

    pem = strip_pem(x)
    return base64.b64decode(pem)

def strip_pem(x):
    if x is None:
        return None

    pem = x.replace('-----BEGIN CERTIFICATE-----', '')
    pem = pem.replace('-----END CERTIFICATE-----', '')
    pem = re.sub(r'-----BEGIN .+?-----', '', pem)
    pem = re.sub(r'-----END .+?-----', '', pem)
    pem = pem.replace(' ', '')
    pem = pem.replace('\t', '')
    pem = pem.replace('\r', '')
    pem = pem.replace('\n', '')
    return pem.strip()

def get_backend(backend=None):
    from cryptography.hazmat.backends import default_backend
    return default_backend() if backend is None else backend

def process_pem_rsakey(data, name, idx):
    from cryptography.hazmat.primitives.serialization import load_der_public_key
    from cryptography.hazmat.primitives.serialization import load_der_private_key
    if data.startswith('-----BEGIN RSA PUBLIC KEY') or data.startswith('-----BEGIN PUBLIC KEY'):
        rsa = load_der_public_key(pem_to_der(data), get_backend())
        public_numbers = rsa.public_numbers()
        return public_numbers.n
    elif data.startswith('-----BEGIN RSA PRIVATE KEY') or data.startswith('-----BEGIN PRIVATE KEY'):
        rsa = load_der_private_key(pem_to_der(data), None, get_backend())
        public_numbers = rsa.private_numbers().public_numbers
        return public_numbers.n
    else:
        return None

def process_x509(x509, name, idx=None, data=None, pem=True, source='', aux=None):
    if x509 is None:
        return

    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
    from cryptography.x509.oid import NameOID

    pub = x509.public_key()
    if not isinstance(pub, RSAPublicKey):
        return

    pubnum = x509.public_key().public_numbers()

    return pubnum.n

def process_pem_cert(data, name, idx):
    from cryptography.x509.base import load_der_x509_certificate
    x509 = load_der_x509_certificate(pem_to_der(data), get_backend())
    return process_x509(x509, name=name, idx=idx, data=data, pem=True, source='pem-cert')

def process_pem(data, name):
    ret = []
    parts = re.split(r'-----BEGIN', data)
    if len(parts) == 0:
        return None

    if len(parts[0]) == 0:
        parts.pop(0)

    crt_arr = ['-----BEGIN' + x for x in parts]
    for idx, pem_rec in enumerate(crt_arr):
        pem_rec = pem_rec.strip()
        if len(pem_rec) == 0:
            continue

        if pem_rec.startswith( '-----BEGIN CERTIF'):
            return process_pem_cert(pem_rec, name, idx)
        elif pem_rec.startswith( '-----BEGIN '):  # fallback
            return process_pem_rsakey(pem_rec, name, idx)
    return ret
#########################################################################################################################


prime_list = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167]
def primorial(n):
    x = 1
    y=1
    for i in range(n):
        x *= prime_list[i]
        y *= (prime_list[i]-1)
    return x,y

def prime_factors(n):
    i = 0
    ans = {}
    for i in range(0,len(prime_list)):
        if((n%prime_list[i])!=0):
            continue
        ans[prime_list[i]]=0
        while((n%prime_list[i])==0):
            n //= prime_list[i]
            ans[prime_list[i]] += 1
    return ans

def element_order(element, modulus, phi_m, phi_m_decomposition):
    if element == 1:
        return 1
    if pow(element, phi_m, modulus) != 1:
        return None
    order = phi_m
    for factor, power in list(phi_m_decomposition.items()):
        for p in range(1, power + 1):
            next_order = order // factor
            if pow(element, next_order, modulus) == 1:
                order = next_order
            else:
                break
    return order

def chinese_remainder(pairs,M): # Mi = M/pi^ei , Mi*yi = 1 mod pi^ei , X = xi*Mi*yi , M is order -- EE720
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

g = 65537
m = primorial(39)[0]
phi_m = primorial(39)[1]
factors_of_phi_m = prime_factors(phi_m)
g_order = element_order(g, m, phi_m, factors_of_phi_m)
factors_of_order = prime_factors(g_order)

fname = sys.argv[1]
fh = open(fname, 'rb')

with fh:
    data = fh.read()
    if data.startswith('0x'):
        data = data[2:]
        print("Size of key: "+str(len(data)*4))
        data = int(data,16) # hex_to_decimal
        d = discrete_log(data, g, g_order, factors_of_order, m)
    elif data.startswith('\\x'):
        data = data[2:]
        print("Size of key: "+str(len(data)*4))
        data = int(data,16) # hex_to_decimal
        d = discrete_log(data, g, g_order, factors_of_order, m)
    else:
        print("Size of key: "+str(len(data)*4))
        data = process_pem(data,fname)
        # print(data)
        d = discrete_log(data, g, g_order, factors_of_order, m)
    if(d is not None):
        print("Key Fingerprinted")
        print("Value of c : "+str(d))
    else:
        print("Key Secure")