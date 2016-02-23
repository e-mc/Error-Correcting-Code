# Error-Correcting-Code
Functions for an Error Correcting Code course

Error correcting codes are used to correct transmission errors in that may occur when transferring data.

-generator.py can generate a generator matrix G for an [n,k] binary code correcting t errors (or return an error message saying 
such a code doesn't exist). G will be printed in standard form (I|A), and can quickly be transformed into a parity matrix 
H = (A^T|I).

The file contains functions to:
 + print a matrix
 + generate a random binary vector
 + create an n x n identity matrix
 + find the pairwise distance between all vectors in a matrix
 + print pairwise distances between vectors
 + check if an [n,k] code correcting t errors is possible
 + a multiplicative formula for the choose(n,r) function
