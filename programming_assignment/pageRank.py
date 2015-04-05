#!/usr/bin/env python
import numpy as np
import scipy.sparse as _sparse
import time
from sklearn.preprocessing import normalize

import optparse, sys, os
from collections import defaultdict


optparser = optparse.OptionParser()
optparser.add_option("-f", "--file", dest="file", default=os.path.join("data","web-Google.txt"), help="data file (default=web-Google.txt)")
(opts, _) = optparser.parse_args()


# this version of page rank is extremely slow with regard to the 
# then define customized functions
def slowReadWebGraph(matSize, filename = os.path.join("data", "web-Google.dat")):
    mat = _sparse.lil_matrix((matSize, matSize))
    sys.stderr.write('Phase 1 - read web graph\n')
    with open(filename, "r") as f:
        for idx, line in enumerate(f):
            data =  line.strip()
            if not data.startswith("#"):
                tmp = data.split('\t')
                col = int(tmp[0])
                row = int(tmp[1])
                mat[row, col] += 1;                
            if idx % 10000 == 0:
                sys.stderr.write('.')
                
    sys.stderr.write('\nPhase 2 - normalize column weight\n')
    
    mat = normalize(mat, norm='l1', axis=0)
    col_nums = np.where(mat.sum(0) == 0)[1]

    N =  mat.shape[0]
    if col_nums.size > 0:
         for col in np.nditer(col_nums):
            mat[:, col] = 1 / float(N)
        
    return mat.tocsc()


def slowPageRank(M_matrix, r_last=0, pTele = 0.2, epsilon = 10**-10, max_iter = sys.maxint):
    sys.stderr.write("Page ranking.")
    M = M_matrix.multiply(1 - pTele)
    iter = 0
    N = M.shape[0]
    while True:
        iter += 1
        sys.stderr.write(".")
        if iter >= max_iter:
            sys.stderr.write("maximum iteration reached.")
            break
        
        r = M.dot(r_last) + pTele / N
        
        if np.absolute( r - r_last).sum() <= epsilon:
            break
        
        r_last = r
        
    return r
        
    

def main():
    start_time = time.time()
    cnt = slowReadBiggestNodesFromGraph(os.path.join("data", "toy.dat"))
    mid_time = time.time()
    elasped_time1 = start_time - mid_time
    print "Finish finding biggest node - elasped time: " + str(elasped_time1)

    graph = slowReadWebGraph(cnt + 1, os.path.join("data", "toy.dat"))
    end_time = time.time()
    elasped_time2 = end_time - mid_time
    print "Finish creating graph - elasped time: " + str(elasped_time2)
    
    r_init = normalize(np.ones((graph.shape[0], 1)), norm='l1', axis=0)

    rank = slowPageRank(graph, r_init)
    final_time = time.time()
    elasped_time3 = final_time - end_time
    print "Computing - elasped time: " + str(elasped_time3)
    print rank



if __name__=="__main__":
	main()
