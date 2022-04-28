import numpy as np


def init(fN, vector_A, vector_B, ref="grid", spacing=1.0):
    """
    Parameters
    ----------
    fN : int
            The number of vertices along the radius of the grid.
    spacing : float
            The distance between to neighnoring vertices in the grid.
    vector_A : float array 3d
            The 1st vector to span the 2D grid.
    vector_B : float array 3d
            The 2nd vector to span the 2D grid.
    ref : str
            Key in the references for the vertices.
    """
    grid = {}
    for dA in np.arange(-fN, fN + 1, 1):
        for dB in np.arange(-fN, fN + 1, 1):
            key = (ref, (dA, dB))
            grid[key] = spacing * (dA * vector_A + dB * vector_B)
    return grid
