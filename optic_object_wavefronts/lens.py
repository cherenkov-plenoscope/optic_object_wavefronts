from . import Mesh
from . import regular_polygon
from . import delaunay
from . import inside_polygon
import numpy as np
import scipy
from scipy import spatial as scipy_spatial


HEXA = np.array([1.0, 0.0, 0.0])
HEXB = np.array([0.5, np.sqrt(3.0) / 2.0, 0.0])


def make_hex_grid(outer_radius=1.0, ref="hex", n=10):
    spacing = float(outer_radius / n)
    N = int(n)
    vertices = {}
    for dA in np.arange(-N, N + 1, 1):
        for dB in np.arange(-N, N + 1, 1):
            bound_upper = -dA + N
            bound_lower = -dA - N
            if dB <= bound_upper and dB >= bound_lower:
                vertices[(ref, (dA, dB))] = (dA * HEXA + dB * HEXB) * spacing
    return vertices


def make_hex_mesh_in_regular_polygon(
    outer_radius, n_poly, n_hex, ref="HexGridInPoly"
):
    g = make_hex_grid(
        outer_radius=outer_radius * 1.5, ref=ref + "/hex", n=n_hex
    )
    r = regular_polygon.make_vertices_xy(
        outer_radius=outer_radius,
        ref=ref + "/ring",
        n=n_poly,
        rot=0.0,
    )

    mesh = Mesh.init()

    mesh["vertices"] = inside_polygon.get_vertices(vertices=g, polygon=r)
    for vkey in r:
        mesh["vertices"][vkey] = r[vkey]

    vnkey = (ref, 0)
    mesh["vertex_normals"][vnkey] = np.array([0.0, 0.0, 1.0])

    faces = delaunay.make_faces_xy(vertices=mesh["vertices"], ref=ref)

    for fkey in faces:
        mesh["faces"][fkey] = {
            "vertices": faces[fkey]["vertices"],
            "vertex_normals": [vnkey, vnkey, vnkey],
        }
    return mesh
