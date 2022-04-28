import numpy as np
import collections
from . import Template


HEXA = np.array([1.0, 0.0, 0.0])
HEXB = np.array([0.5, np.sqrt(3.0) / 2.0, 0.0])


def init_from_outer_radius(outer_radius=1.0, ref="hex", fn=10):
    spacing = float(outer_radius / fn)
    N = int(fn)
    vertices = collections.OrderedDict()
    for dA in np.arange(-N, N + 1, 1):
        for dB in np.arange(-N, N + 1, 1):
            bound_upper = -dA + N
            bound_lower = -dA - N
            if dB <= bound_upper and dB >= bound_lower:
                vertices[(ref, (dA, dB))] = (dA * HEXA + dB * HEXB) * spacing
    return vertices


def init_from_spacing(spacing=1.0, ref="hex", fN=10):
    """
    Parameters
    ----------
    spacing : float
            The distance between to neighnoring vertices in the grid.
    fN : int
            The number of vertices along the radius of the grid.
    ref : str
            Key in the references for the vertices.

    The vertices are the centers of the hexagons.
    The central vertex is in the origin.

          Y
         _|_
     ___/ | \___
    /   \_|_/   \
    \___/ |_\___/____ x
    /   \___/   \
    \___/   \___/
        \___/
    """
    return Template.init(
        fN, vector_A=HEXA, vector_B=HEXB, ref=ref, spacing=spacing
    )
