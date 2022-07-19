import numpy as np
import os
import scipy
from scipy import spatial as scipy_spatial
from . import polygon


def make_faces_xy(vertices, ref):
    """
    Create triangular faces based on the vertices x, and y components.

    Parameters
    ----------
    vertices : dict
            The vertices to make triangular faces for.
    ref : str
            The key for the faces keys.

    Returns
    -------
    faces : dict
            The faces for the vertices, referencing the vertices by key.
    """
    vkeys, vertices = polygon.to_keys_and_numpy_array(polygon=vertices)
    vertices_xy = vertices[:, 0:2]

    del_tri = scipy.spatial.Delaunay(points=vertices_xy)
    del_faces = del_tri.simplices

    faces = {}
    for fidx, del_face in enumerate(del_faces):
        fkey = os.path.join(ref, "{:06d}".format(fidx))
        faces[fkey] = {
            "vertices": [
                vkeys[del_face[0]],
                vkeys[del_face[1]],
                vkeys[del_face[2]],
            ],
        }
    return faces
