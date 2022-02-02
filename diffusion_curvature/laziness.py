# AUTOGENERATED! DO NOT EDIT! File to edit: 03_laziness_decay.ipynb (unless otherwise specified).

__all__ = ['curvature', 'laziness_decay']

# Cell
import numpy as np
def curvature(P, diffusion_powers=8, aperture = 20, smoothing=1, verbose = False, return_density = False, dynamically_adjusting_neighborhood = False, precomputed_powered_P = None, non_lazy_diffusion=False):
    """Diffusion Laziness Curvature
    Estimates curvature by measuring the amount of mass remaining within an initial neighborhood after t steps of diffusion. Akin to measuring the laziness of a random walk after t steps.

    Parameters
    ----------
    P : n x n ndarray
        The diffusion matrix of the graph
    diffusion_powers : int, optional
        Number of steps of diffusion to take before measuring the laziness, by default 8
    aperture : int, optional
        The size of the initial neighborhood, from which the percentage of mass remaining in this neighborhood is calculated, by default 20
    smoothing : int, optional
        Amount of smoothing to apply. Currently works by multiplying the raw laziness values with the diffusion operator, as a kind of iterated weighted averaging; by default 1
    verbose : bool, optional
        Print diagnostics, by default False
    return_density : bool, optional
        Return the number of neighbors each point shares, by default False
    dynamically_adjusting_neighborhood : bool, optional
        Whether to give each point the same initial neighborhood size, by default False
    precomputed_powered_P : ndarray, optional
        Optionally pass a precomputed powered diffusion operator, to speed up computation, by default None

    Returns
    -------
    length n array
        The laziness curvature values for each point
    """
    # the aperture sets the size of the one-hop neighborhood
    # the aperture parameter is the average number of neighbors to include, based off of the sorted diffusion values
    # Set thresholds as the kth largest diffusion value, presumed to be held by the kth nearest neighbor.
    thresholds = np.partition(P,-aperture)[:,-aperture]
    # thresholds = np.sort(P)[:,-aperture]
    if verbose: print(thresholds)
    if dynamically_adjusting_neighborhood:
        P_thresholded = (P >= thresholds[:,None]).astype(int)
    else:
        P_threshold = np.mean(thresholds) # TODO could also use min
        P_thresholded = (P >= P_threshold).astype(int)
        if verbose: print("Derived threshold ",P_threshold)

    if verbose: print(np.sum(P_thresholded,axis=1))
    if verbose: print("Performing matrix powers...")

    if precomputed_powered_P is not None:
        P_powered = precomputed_powered_P
    elif non_lazy_diffusion:
        print("Removing self-diffusion")
        P_zero_diagonal = (np.ones_like(P) - np.diag(np.ones(len(P))))*P
        D = np.diag(1/np.sum(P_zero_diagonal,axis=0))
        P = D @ P_zero_diagonal
        P_powered = np.linalg.matrix_power(P,diffusion_powers)
    else:
        P_powered = np.linalg.matrix_power(P,diffusion_powers)
    # take the diffusion probs of the neighborhood
    near_neighbors_only = P_powered * P_thresholded
    laziness_aggregate = np.sum(near_neighbors_only,axis=1)
    laziness = laziness_aggregate
    if smoothing: # TODO there are probably more intelligent ways to do this smoothing
        # Local averaging to counter the effects local density
        if verbose: print("Applying smoothing...")
        smoothing_P_powered = np.linalg.matrix_power(P,smoothing)
        average_laziness = smoothing_P_powered @ laziness_aggregate[:,None]
        average_laziness = average_laziness.squeeze()
        laziness = average_laziness
    if return_density:
        # compute sums of neighbors taken into consideration
        ones_matrix = np.ones_like(P_thresholded)
        ones_remaining = ones_matrix * P_thresholded
        local_density = np.sum(ones_remaining,axis=1)
        return laziness, local_density
    return laziness

# Cell
def laziness_decay(P, max_steps = 32, aperture = 20, smoothing=1, adaptive_neighborhood = False, non_lazy_diffusion=False):
    """Generates a matrix of the decaying laziness value per point over a range of t values

    Parameters
    ----------
    P : ndarray
        Diffusion matrix
    max_steps : int, optional
        Number of diffusion steps to take (starting from 1), by default 32
    aperture : int, optional
        The size of the initial diffusion neighborhood, by default 20
    smoothing : int, optional
        Number of smmoothing interations, by default 1

    Returns
    -------
    ndarray
        Each column is a set of laziness values per point at a specific time.
    """
    decay_per_point = np.empty((len(P),max_steps))
    if non_lazy_diffusion:
        print("Removing self-diffusion")
        P_zero_diagonal = (np.ones_like(P) - np.diag(np.ones(len(P))))*P
        D = np.diag(1/np.sum(P_zero_diagonal,axis=0))
        P = D @ P_zero_diagonal
    P_t = P
    for t in range(1,max_steps+1):
        P_t = P_t @ P
        laziness = curvature(P,diffusion_powers=t,aperture=aperture,precomputed_powered_P=P_t,smoothing=smoothing,dynamically_adjusting_neighborhood=adaptive_neighborhood, non_lazy_diffusion=non_lazy_diffusion)
        decay_per_point[:,t-1] = laziness
    return decay_per_point