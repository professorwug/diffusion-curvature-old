# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_datasets.ipynb.

# %% auto 0
__all__ = ['rejection_sample_for_torus', 'torus', 'rejection_sample_for_hyperboloid', 'hyperboloid',
           'rejection_sample_for_ellipsoid', 'ellipsoid', 'sphere', 'rejection_sample_for_saddle', 'paraboloid',
           'plane']

# %% ../01_datasets.ipynb 2
import numpy as np
from .core import plot_3d
from nbdev.showdoc import *

# %% ../01_datasets.ipynb 16
import numpy as np
def rejection_sample_for_torus(n, r, R):
    # Rejection sampling torus method [Sampling from a torus (Revolutions)](https://blog.revolutionanalytics.com/2014/02/sampling-from-a-torus.html)
    xvec = np.random.random(n) * 2 * np.pi
    yvec = np.random.random(n) * (1/np.pi)
    fx = (1 + (r/R)*np.cos(xvec)) / (2*np.pi)
    return xvec[yvec < fx]

def torus(n=2000, c=2, a=1, noise=None, seed=None, use_guide_points = False):
    """
    Sample `n` data points on a torus. Modified from [tadasets.shapes — TaDAsets 0.1.0 documentation](https://tadasets.scikit-tda.org/en/latest/_modules/tadasets/shapes.html#torus)
    Uses rejection sampling.

    In addition to the randomly generated points, a few constant points have been added.
    The 0th point is on the outer rim, in a region of high positive curvature. The 1st point is in the inside, in a region of negative curvature, and the 2nd point is on the top, where the curvature should be closer to zero.

    Parameters
    -----------
    n : int
        Number of data points in shape.
    c : float
        Distance from center to center of tube.
    a : float
        Radius of tube.
    ambient : int, default=None
        Embed the torus into a space with ambient dimension equal to `ambient`. The torus is randomly rotated in this high dimensional space.
    seed : int, default=None
        Seed for random state.
    """

    assert a <= c, "That's not a torus"

    np.random.seed(seed)
    theta = rejection_sample_for_torus(n-2, a, c)
    phi = np.random.random((len(theta))) * 2.0 * np.pi

    data = np.zeros((len(theta), 3))
    data[:, 0] = (c + a * np.cos(theta)) * np.cos(phi)
    data[:, 1] = (c + a * np.cos(theta)) * np.sin(phi)
    data[:, 2] = a * np.sin(theta)

    if use_guide_points:
        data = np.vstack([[[0,-c-a,0],[0,c-a,0],[0,c,a]],data])

    if noise:
        data += noise * np.random.randn(*data.shape)

    # compute curvature of sampled torus
    ks = 8*np.cos(theta)/(5 + np.cos(theta))

    return data, ks

# %% ../01_datasets.ipynb 24
def rejection_sample_for_hyperboloid(n,a,b,c,u_limit):
    theta = np.random.random(n)*2*np.pi
    u = (np.random.random(n)*2 - 1)*u_limit
    fx = np.sqrt(a**2 * b**2 * u**2 + a**2 * u**2 * np.sin(theta)**2 + a**2 * np.sin(theta)**2  - b**2 * u**2 * np.sin(theta)**2 + b**2 * u**2 - b**2 * np.sin(theta)**2 + b**2) 
    yvec = np.random.random(n) * (1/np.max(fx))
    return theta[yvec < fx], u[yvec < fx]

def hyperboloid(n=2000,a=2,b=2,c=1, u_limit = 2, seed=None):
    """Sample roughly n points on a hyperboloid, using rejection sampling.

    Parameters
    ----------
    n : int, optional
        number of points, by default 2000
    a : int, optional
        hyperboloid param1, by default 2
    b : int, optional
        hyperboloid param2, by default 2
    c : int, optional
        stretchiness in z, by default 1
    u_limit : int, optional
        Constrain the free parameter u to [-l,l], by default 2
    seed : int, optional
        For repeatability, seed the randomness, by default None

    Returns
    -------
    The sampled points, and the curvatures of each point
    """

    np.random.seed(seed)
    theta, u = rejection_sample_for_hyperboloid(n,a,b,c,u_limit)
    data = np.zeros((len(theta), 3))
    data[:, 0] = a*np.cos(theta)*np.sqrt(u**2 + 1)
    data[:, 1] = b*np.sin(theta)*np.sqrt(u**2 + 1)
    data[:, 2] = c*u

    # compute curvature of sampled hyperboloid
    ks = -(2/(5*data[:,2]**2 + 1)**2)

    return data, ks

# %% ../01_datasets.ipynb 30
def rejection_sample_for_ellipsoid(n,a,b,c):
    theta = np.random.random(n)*2*np.pi
    phi = np.random.random(n)*2*np.pi
    fx = np.sqrt(-a**2 * b**2 * np.sin(phi)**4 + a**2 * b**2 * np.sin(phi)**2 + a**2 * c**2 * np.sin(phi)**4 * np.sin(theta)**2 - b**2 * c**2 * np.sin(phi)**4 * np.sin(theta)**2 + b**2 * c**2 * np.sin(phi)**4)
    yvec = np.random.random(n) * (1/np.max(fx))
    return theta[yvec < fx], phi[yvec < fx]

def ellipsoid(n=2000,a=3,b=2,c=1, seed=None, noise=None):
    """Sample roughly n points on an ellipsoid, using rejection sampling.

    Parameters
    ----------
    n : int, optional
        number of points, by default 2000
    a : int, optional
        ellipsoid param1, by default 3
    b : int, optional
        ellipsoid param2, by default 2
    c : int, optional
        stretchiness in z, by default 1
    seed : int, optional
        For repeatability, seed the randomness, by default None

    Returns
    -------
    The sampled points, and the curvatures of each point
    """

    np.random.seed(seed)
    theta, phi = rejection_sample_for_ellipsoid(n,a,b,c)
    data = np.zeros((len(theta), 3))
    data[:, 0] = a*np.cos(theta)* np.sin(phi)
    data[:, 1] = b*np.sin(theta)*np.sin(phi)
    data[:, 2] = c*np.cos(phi)

    # compute curvature of sampled torus (gaussian curvature)
    ks = 2* (a**2 * b**2 * c**2) / (a**2 * b**2 * np.cos(phi)**2 + c**2 * (b**2 * np.cos(theta)**2 + a**2 * np.sin(theta)**2)*np.sin(phi)**2)**2
    
    # add noise to data, if needed
    if noise:
        noise = np.random.randn(len(data),3)*noise
        data = data + noise
    
    return data, ks

# %% ../01_datasets.ipynb 34
def sphere(n, radius=1,noise=0, use_guide_points = False):
    if use_guide_points:
        n = n - 1
    u = np.random.normal(0,1,size=(n))
    v = np.random.normal(0,1,size=(n))
    w = np.random.normal(0,1,size=(n))
    norm = (u*u + v*v + w*w)**(0.5)
    (x,y,z) = (u,v,w)/norm
    X = np.column_stack([x,y,z])
    if use_guide_points:
        X = np.vstack([np.array([0,0,1]),X])
    ks = np.ones(n)*2
    return X, ks

# %% ../01_datasets.ipynb 42
def rejection_sample_for_saddle(n,a,b):
    x = np.random.random(n)*2 - 1 # random values in -1, 1
    y = np.random.random(n)*2 - 1
    fx = np.sqrt(4*a**2*x**2 + 4*b**2*y**2 + 1)
    yvec = np.random.random(n) * (1/np.max(fx))
    return x[yvec < fx], y[yvec < fx]

def paraboloid(n=2000,a=1,b=-1, seed=None, use_guide_points = False):
    """Sample roughly n points on a saddle, using rejection sampling for even density coverage
    Defined by $ax^2 + by^2$. 

    Parameters
    ----------
    n : int, optional
        number of points, by default 2000
    a : int, optional
        ellipsoid param1, by default 1
    b : int, optional
        ellipsoid param2, by default -1
    seed : int, optional
        For repeatability, seed the randomness, by default None

    Returns
    -------
    The sampled points, and the curvatures of each point
    """
    if use_guide_points:
        n = n - 1
    np.random.seed(seed)
    x, y = rejection_sample_for_saddle(n,a,b)
    if use_guide_points:
        x = np.concatenate([[0],x])
        y = np.concatenate([[0],y])
    data = np.zeros((len(x), 3))
    data[:, 0] = x
    data[:, 1] = y
    data[:, 2] = a*x**2 + b*y**2
    # compute curvature of sampled saddle region
    # TODO: Compute gaussian curvature
    # TODO: Currently assuming that b is negative (hyperbolic paraboloid)
    ap = np.sqrt(1/a) 
    bp = b/np.abs(b) * np.sqrt(1/np.abs(b))
    ks = -(4*a**6 * b**6)/(a**4*b**4 + 4*b**4*x**2+4*a**4*y**2)**2
    
    return data, ks

# %% ../01_datasets.ipynb 51
def plane(n):
    coords_2d = np.random.rand(n,2)*2-1
    coords_2d = np.vstack([np.zeros(2),np.array([0,0.2]),np.array([0,-0.2]),np.zeros(2),coords_2d])
    return coords_2d
