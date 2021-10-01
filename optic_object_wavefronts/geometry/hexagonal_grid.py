import numpy as np
import collections

HEXA = np.array([1.0, 0.0, 0.0])
HEXB = np.array([0.5, np.sqrt(3.0) / 2.0, 0.0])


def make_vertices_xy(outer_radius=1.0, ref="hex", n=10):
    spacing = float(outer_radius / n)
    N = int(n)
    vertices = collections.OrderedDict()
    for dA in np.arange(-N, N + 1, 1):
        for dB in np.arange(-N, N + 1, 1):
            bound_upper = -dA + N
            bound_lower = -dA - N
            if dB <= bound_upper and dB >= bound_lower:
                vertices[(ref, (dA, dB))] = (dA * HEXA + dB * HEXB) * spacing
    return vertices
