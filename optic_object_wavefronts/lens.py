from . import Mesh
from . import regular_polygon
from . import delaunay
from . import hexagonal_grid
from . import inside_polygon
import numpy as np


def make_hex_mesh_in_regular_polygon(
    outer_radius, n_poly, n_hex, ref="HexGridInPoly"
):
    g = hexagonal_grid.make_vertices_xy(
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
