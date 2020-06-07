### Requirements
1. `python 2.7`
2. `sage` - Can be installed using the command: `sudo apt install sagemath` (Ubuntu 18.04).

### key_generation.sage
It takes key-size as input and outputs p,q and N.

### fingerprinting.py
It finds the value of 'c', if exists, using pohlig-hellman algorithm.

Path of file of RSA key (.txt for hex or .pem) should be given as command-line argument.

Example :- python fingerprinting.py cert01.pem

### fingerprinting.sage
It also does the same task as fingerprinting.py. It will ask for the value of N as input.

Example :- sage fingerprinting.sage

### optimisingM_bruteforce.sage
It calculates the value of optimised M' for 512-bit public key using brute-force method.

Takes around 5.25 sec.

### optimisingM.sage
It calculates the value of optimised M' for any key size using the greedy algorithm. It will ask size of N as input.

Takes some seconds to compute M'.

### attack.sage
It factorises N to p & q. It takes N and p mod M' as input. It is an implementation of Coppersmith's algorithm.

M' is given as output by the code, so user can calculate p mod M' and give it as input.

### LLL.py
It is the implementation of LLL algorithm.

### Full_attack.sage
It factorises N into p & q taking only N as input.
