import numpy as np
import scipy
from scipy import spatial as scipy_spatial


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
    vertices_xy = []
    vkeys = []
    for vkey in vertices:
        vkeys.append(vkey)
        vertices_xy.append(vertices[vkey][0:2])
    vertices_xy = np.array(vertices_xy)

    del_tri = scipy.spatial.Delaunay(points=vertices_xy)
    del_faces = del_tri.simplices

    faces = {}
    for fidx, del_face in enumerate(del_faces):
        fkey = (ref, fidx)
        faces[fkey] = {
            "vertices": [
                vkeys[del_face[0]],
                vkeys[del_face[1]],
                vkeys[del_face[2]],
            ],
        }
    return faces
