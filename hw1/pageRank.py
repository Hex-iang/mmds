#!/usr/bin/env python
import numpy as np
import scipy.sparse as _sparse
import time
import optparse, sys, os, copy
from collections import defaultdict


optparser = optparse.OptionParser()
optparser.add_option("-f", "--file", dest="file", default=os.path.join("data","web-Google.txt"), help="data file (default=web-Google.txt)")
(opts, _) = optparser.parse_args()


# then define customized functions
def readWebGraph(matSize, filename = os.path.join("data", "web-Google.txt")):
    mat = _sparse.lil_matrix((matSize, matSize), dtype=np.float32)
    with open(filename, "r") as f:
        for idx, line in enumerate(f):
            data =  line.strip()
            if not data.startswith("#"):
                tmp = data.split('\t')
                row = int(tmp[0])
                col = int(tmp[1])
                mat[row, col] += 1;                
            if idx % 10000 == 0:
                sys.stderr.write('.')
    return mat.tocsr()

# count the largest graph node number
def readBiggestNodesFromGraph(filename = os.path.join("data", "web-Google.txt")):
    max_node = 0
    with open(filename, "r") as f:
        for idx, line in enumerate(f):
            data =  line.strip()
            if not data.startswith("#"):
                tmp = data.split('\t')
                max_node = max(int(tmp[0]), int(tmp[1]), max_node)
            if idx % 1000000 == 0:
                sys.stderr.write('.')
                
    return max_node



def main():
	start_time = time.time()
	cnt = readBiggestNodesFromGraph()
	mid_time = time.time()
	elasped_time1 = start_time - mid_time
	print "Finish finding biggest node - elasped time: " + str(elasped_time1)

	graph = readWebGraph(cnt + 1)
	end_time = time.time()
	elasped_time2 = mid_time - end_time
	print "Finish creating graph - elasped time: " + str(elasped_time2)



if __name__=="__main__":
	main()
