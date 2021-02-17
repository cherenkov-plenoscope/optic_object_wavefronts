import numpy as np


def make_vertices_xy(outer_radius=1.0, ref="ring", n=16, rot=0.0):
    vertices = {}
    for nphi, phi in enumerate(
        np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    ):
        vertices[(ref, nphi)] = np.array(
            [
                outer_radius * np.cos(rot + phi),
                outer_radius * np.sin(rot + phi),
                0.0
            ]
        )
    return vertices


def inner_radius(n):
    return 1.0 * np.cos(np.pi / n)
