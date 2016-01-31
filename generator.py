import random
import time
import math
from operator import add

def choose(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

def isCodePossible(n,k,t):
    # t is the max number of errors an [n,k] code can correct
    # for a given code to exist, it must satisfy the 
    # sphere-packing bound
    codewords_possible = pow(2,n)
    codewords_needed = 0
    
    for i in range(t+1):
        codewords_needed += choose(n,i)
    codewords_needed *= pow(2,k)

    # note: if codewords_needed == codewords_possible,
    # the code is "perfect"
    if (codewords_needed <= codewords_possible):
        return True
    return False
    

def isPower_of_2(num):
    if (math.log(num,2) != math.ceil(num,2)):
        return False
    return True

# calculate the distance between two binary vectors
def vectordistance(vec1, vec2):
    if (len(vec1) != len(vec2)):
        print "Vectors must be the same size."
    
    dist = 0 
    for k in range(len(vec1)):            
        dist += ((vec1[k]+vec2[k])%2)
    return dist

# generate a random binary vector of specified length
def newvector(vec_length):
    random.seed()
    vect = []
    for j in range(vec_length):
        vect.append(random.randint(0,1))
    return vect

# generate a dim x dim identity matrix
def make_Identity_Matrix(dim):
    I = [[0 for col in range(dim)] for row in range(dim)]
    for i in range(dim):
        I[i][i] = 1
    return I

# dist(u,v) = wt(u-v), and u-v is a linear combination of two codewords
# thus, the minimum distance is the weight of the least-weight codeword
def minimum_linear_combo_wt(Matrix, d):
    length = len(Matrix)                    # number of rows in Matrix
    counter = [0 for col in range(length)]  # count up in binary. counter[0] = MSB
    counter[length-1] = 1                   # we don't consider the 0 vector when calculating min weights
    complete = [1 for col in range(length)] # stop counting once all 1's
    while (counter != complete):
        lin_combo = [0 for col in range(len(Matrix[0]))]
        for j in range(length):
            if (counter[j] == 1):
                #print lin_combo," + ",Matrix[j]
                lin_combo = map(add, lin_combo, Matrix[j])
        lin_combo = [lin_combo[col]%2 for col in range(len(Matrix[0]))]
        # we mod by 2 b/c these are binary codewords

        wt = lin_combo.count(1) # count the number of 1's, i.e. the weight
        if (wt < d):            # if weight is less than the allowable distance, code fails
            return False

        # the following increments our binary counter array
        carry = (1 & counter[length-1])
        counter[length-1] = counter[length-1] ^ 1
        
        for i in range(length-2,-1,-1):
            ncount = carry ^ counter[i]
            ncarry = carry & counter[i]
            counter[i] = ncount
            carry = ncarry            
    return True
    
# generate the generator matrix G for a binary code correcting t errors
def generate_codewords(n, k, t):
    I = make_Identity_Matrix(k)
    G = [I[row]+newvector(n-k) for row in range(k)]
    d = 2*t + 1
    # d is min distance between any two codewords
    # given that the code corrects t errors

    # generate new codes until they satisfy the minimum distance requirement
    while(not minimum_linear_combo_wt(G, d)):
        G = [I[row]+newvector(n-k) for row in range(k)]
    return G
    
# prints out a matrix row by row
def printMatrix(Matrix):
    for i in range(len(Matrix)):
        print Matrix[i]

# print pairwise distances for all vectors in a matrix
# (except for a vector and itself, which always = 0)
def printDistances(vectors):
    vec_size = len(vectors)
    
    for i in range(vec_size):
        for j in range(vec_size):
            if (i != j):
                print "dist(",i+1,",",j+1,") = ",vectordistance(vectors[i],vectors[j])

def main():
    print ("This program will print a generator matrix for an [n,k] binary "
           "code. k denotes the number of info bits, n is the length of each "
           "codeword (there are n-k redundancy bits), and t is the number of "
           "errors the code can correct.")
           
       
    n = input("Please enter an n value: ")
    k = input("Please enter a k value: ")
    t = input("Please enter a t value: ")
    if (isCodePossible(n,k,t) == False):
        print "Code is not possible by the sphere-packing bound thm."
        return
    
    G = generate_codewords(n,k,t)
    printMatrix(G)

    
if __name__ == '__main__':
    #start = time.time()
    main()
    #print "Total run time is: ", time.time() - start
