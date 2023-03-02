# AUTOGENERATED! DO NOT EDIT! File to edit: ../05b_gaussian_invariance.ipynb.

# %% auto 0
__all__ = ['compute_anisotropic_affinities_from_graph', 'compute_anisotropic_diffusion_matrix_from_graph',
           'gaussian_invariant_curvature_of_graph']

# %% ../05b_gaussian_invariance.ipynb 11
import numpy as np
def compute_anisotropic_affinities_from_graph(
    A:np.ndarray, # the adjacency/affinity matrix of the graph
    alpha:float, # the anisotropic density normalization parameter
) -> np.ndarray:
    # normalize by density
    D = np.diag(1/np.sum(A,axis=1)**alpha)
    A_anis = D @ A @ D
    return A_anis

def compute_anisotropic_diffusion_matrix_from_graph(
    A:np.ndarray, # the adjacency/affinity matrix of the graph
    alpha:float, # the anisotropic density normalization parameter
    ) -> np.ndarray:
    A_anis = compute_anisotropic_affinities_from_graph(A,alpha)
    # row normalize to create diffusion matrix
    D = np.diag(1/np.sum(A_anis,axis=1))
    P = D @ A_anis
    return P

# %% ../05b_gaussian_invariance.ipynb 12
def gaussian_invariant_curvature_of_graph(
    A:np.ndarray, # adjacency/affinity matrix. Must be based on anisotropic kernel for theory to work.
    t:int = 5,
    k:int = 4,
    return_avg:bool = True, # whether to average the scalar curvature values to combat local density
    ):
    """
    Computes a signed point-wise curvature estimate by comparing the 
    product of 2 diffusions with the half-time diffusion.
    In euclidean space, these should be equal.
    """
    # calculate anisotropic diffusion matrix
    P = compute_anisotropic_diffusion_matrix_from_graph(A, alpha=1)
    # Get pairs of opposing neighbors for each point
    op = get_opposing_points_from_graph_neighbors(P,k=k,t=1)
    # perform two iterations of diffusion
    Pt1 = np.linalg.matrix_power(P,t)
    Pt2 = np.linalg.matrix_power(Pt1,t)
    # for each set of opposing neighbors, extract the larger scale diffusion at that point
    P_t2_op1 = Pt2[op[:,:,0]]
    P_t2_op2 = Pt2[op[:,:,1]]
    # take the product of these, and normalize to sum to one
    P_t2_products = P_t2_op1 * P_t2_op2
    P_t2_products = P_t2_products / np.sum(P_t2_products,axis=2)[:,:,None]
    # extract the halved diffusion from the (likely) midpoint
    P_t1_midpoint_halved = np.repeat(Pt1[:,None,:],[k],axis=1)
    # take the differences between these
    curvature_diffs = np.sum(P_t2_products - P_t1_midpoint_halved,axis=2)
    # sum them for the scalar curvature
    scalar_k = np.sum(curvature_diffs,axis=1)/k
    if return_avg:
        # average scalar k
        scalar_k_avg = scalar_k @ P 
        return scalar_k_avg, curvature_diffs
    else:
        return scalar_k, curvature_diffs

