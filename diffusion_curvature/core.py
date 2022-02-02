# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['DiffusionMatrix', 'plot_3d']

# Cell
import numpy as np
from sklearn.metrics import pairwise_distances
def DiffusionMatrix(X, kernel_type = "fixed", sigma = 0.7, k = 3, alpha = 0.5, nn=5):
    """
    Given input X returns a diffusion matrix P, as an numpy ndarray.
    X is a numpy array of size n x d
    kernel_type is a string, either "fixed" or "adaptive" or "anisotropic" or "adaptive anisotropic"
    sigma is the non-adaptive gaussian kernel parameter
    k is the adaptive kernel parameter
    Returns:
    P is a numpy array of size n x n that is the diffusion matrix
    """
    # construct the distance matrix
    D = pairwise_distances(X)
    # make the affinity matrix
    if kernel_type == "fixed":
        W = (1/sigma*np.sqrt(2*np.pi))*np.exp(-D**2/(2*sigma**2))
    elif kernel_type == "adaptive" or kernel_type == "adaptive anisotropic":
        # Get the distance to the kth neighbor
        distance_to_k_neighbor = np.partition(D,k)[:,k]
        # Populate matrices with this distance for easy division.
        div1 = np.ones(len(D))[:,None] @ distance_to_k_neighbor[None,:]
        div2 = distance_to_k_neighbor[:,None] @ np.ones(len(D))[None,:]
        print("Distance to kth neighbors",distance_to_k_neighbor)
        # compute the gaussian kernel with an adaptive bandwidth
        W = (1/2*np.sqrt(2*np.pi))*(np.exp(-D**2/(2*div1**2))/div1 + np.exp(-D**2/(2*div2**2)/div2))
        if kernel_type == "adaptive anisotropic":
            # Additional normalization step for density
            D = np.diag(1/np.sum(W,axis=1))
            W = D @ W @ D
    elif kernel_type == "nearest neighbor":
        pass
    elif kernel_type == "anisotropic":
        W1 = np.exp(-D**2/(2*sigma**2))
        D = np.diag(1/np.sum(W1,axis=1))
        W = D @ W1 @ D
    elif kernel_type == "alpha-decay":
        distance_to_k_neighbor = tf.nn.top_k(D, k = k, sorted = True).values[:,-1]
        distance_to_k_neighbor = tf.cast(distance_to_k_neighbor,tf.float32)
        D = tf.cast(D, tf.float32)
        div1 = tf.linalg.matmul(tf.ones(len(D))[:,None], distance_to_k_neighbor[None,:])
        div2 = tf.linalg.matmul(distance_to_k_neighbor[:,None],tf.ones(len(D))[None,:])
        W = 0.5*(tf.exp(-(D/div1)**alpha) + tf.exp(-(D/div2)**alpha))
    else:
        raise ValueError("kernel_type must be either 'fixed' or 'adaptive'")
    # turn affinity matrix into diffusion matrix
    D = np.diag(1/np.sum(W,axis=1))
    P = D @ W
    return P

# Cell
# For plotting 2D and 3D graphs
import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def plot_3d(X,distribution=None, title="",lim=None,use_plotly=False):
    if distribution is None:
        distribution = np.zeros(len(X))
    if lim is None:
        lim = np.max(np.linalg.norm(X,axis=1))
    if use_plotly:
        d = {'x':X[:,0],'y':X[:,1],'z':X[:,2],'colors':distribution}
        df = pd.DataFrame(data=d)
        fig = px.scatter_3d(df, x='x',y='y',z='z',color='colors', title=title, range_x=[-lim,lim], range_y=[-lim,lim],range_z=[-lim,lim])
        fig.show()
    else:
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111,projection='3d')
        ax.axes.set_xlim3d(left=-lim, right=lim)
        ax.axes.set_ylim3d(bottom=-lim, top=lim)
        ax.axes.set_zlim3d(bottom=-lim, top=lim)
        ax.scatter(X[:,0],X[:,1],X[:,2],c=distribution)
        ax.set_title(title)
        plt.show()