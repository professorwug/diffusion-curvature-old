import numpy as np
from scipy.sparse import bsr_array
# Diffusion curvature relies on a few numpy matrix tricks. Let's see if they can be ported easily to csr format

# Make a matrix with a lot of zero values, by randomly initializing it and blocking off 80% of the values to be zero
P = np.random.rand(10000,10000)
P[P > 0.2] = 0

# Make this matrix sparse with the Block Compressed Row format
sP = bsr_array(P)

# Challenge 1. Partitioning the matrix to find the average threshold value.
# The .data returns just the nonzero values of the given row. We're just finding the kth biggest value, so that's perfect.
i = 10
aperture = 15
row_partition = np.partition(sP.getrow(i).data,-aperture)[-aperture]
print(row_partition)
breakpoint()

sP_t = (sP >= row_partition).astype(int)


# most efficient to do this for some representative sample of the points, rather than trying to do it for every point. We just need the mean.
