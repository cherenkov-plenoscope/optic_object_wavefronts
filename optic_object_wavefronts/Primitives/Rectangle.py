from .. import Object
from .. import Geometry
from .. import Delaunay
import numpy as np


def init(
    x_width=4 / 3, y_width=1, ref="rect",
):
    """
    Returns a rectangle-object.

    2D surface
    1 Material

    Parameters
    ----------
    x_width : float
            Width in x.
    y_width : float
            Width in y.
    ref : str
            Key for the material.
    """
    obj = Object.init()
    obj["vertices"][(ref, 0)] = 0.5 * np.array([+x_width, +y_width, 0])
    obj["vertices"][(ref, 1)] = 0.5 * np.array([-x_width, +y_width, 0])
    obj["vertices"][(ref, 2)] = 0.5 * np.array([-x_width, -y_width, 0])
    obj["vertices"][(ref, 3)] = 0.5 * np.array([+x_width, -y_width, 0])

    vnkey = (ref, 0)
    obj["vertex_normals"][vnkey] = np.array([0.0, 0.0, 1.0])

    obj["faces"][(ref, 0)] = {
        "vertices": [(ref, 0), (ref, 1), (ref, 2)],
        "vertex_normals": [vnkey, vnkey, vnkey],
    }
    obj["faces"][(ref, 1)] = {
        "vertices": [(ref, 2), (ref, 3), (ref, 0)],
        "vertex_normals": [vnkey, vnkey, vnkey],
    }
    obj["materials"][ref] = [ref]
    return obj
