# AUTOGENERATED! DO NOT EDIT! File to edit: 01_datasets.ipynb (unless otherwise specified).

__all__ = ['rejection_sample_for_torus', 'torus', 'rejection_sample_for_hyperboloid', 'hyperboloid',
           'rejection_sample_for_ellipsoid', 'ellipsoid']

# Cell
import numpy as np
from .core import plot_3d
from nbdev.showdoc import *

# Cell
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

# Cell
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

    # compute curvature of sampled torus
    ks = -(2/(5*data[:,2]**2 + 1)**2)

    return data, ks

# Cell
def rejection_sample_for_ellipsoid(n,a,b,c):
    theta = np.random.random(n)*2*np.pi
    phi = np.random.random(n)*2*np.pi
    fx = np.sqrt(-a**2 * b**2 * np.sin(phi)**4 + a**2 * b**2 * np.sin(phi)**2 + a**2 * c**2 * np.sin(phi)**4 * np.sin(theta)**2 - b**2 * c**2 * np.sin(phi)**4 * np.sin(theta)**2 + b**2 * c**2 * np.sin(phi)**4)
    yvec = np.random.random(n) * (1/np.max(fx))
    return theta[yvec < fx], phi[yvec < fx]

def ellipsoid(n=2000,a=3,b=2,c=1, seed=None):
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

    return data, ks