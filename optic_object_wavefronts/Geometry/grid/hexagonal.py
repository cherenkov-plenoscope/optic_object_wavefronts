import numpy as np
import os
import collections
from . import template


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
                vkey = os.path.join(ref, "{:d}_{:d}".format(dA, dB))
                vertices[vkey] = (dA * HEXA + dB * HEXB) * spacing
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
    return template.init(
        fN, vector_A=HEXA, vector_B=HEXB, ref=ref, spacing=spacing
    )


def estimate_spacing_for_small_hexagons_in_big_hexagon(
    big_hexagon_outer_radius, num_small_hexagons_on_diagonal_of_big_hexagon,
):
    assert big_hexagon_outer_radius > 0.0

    n = num_small_hexagons_on_diagonal_of_big_hexagon
    assert n > 0
    assert np.mod(n, 2) == 1

    big_hexagon_inner_radius = big_hexagon_outer_radius * np.sqrt(3) / 2

    num_outer_diagonals = np.ceil(n / 2)
    num_radii = np.floor(n / 2)

    outer_diagonal_weight = 2.0 / np.sqrt(3)
    radii_weight = 1.0 / np.sqrt(3)

    spacing = (2 * big_hexagon_inner_radius) / (
        num_outer_diagonals * outer_diagonal_weight + num_radii * radii_weight
    )
    return spacing
