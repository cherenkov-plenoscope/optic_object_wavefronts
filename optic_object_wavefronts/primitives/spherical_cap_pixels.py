from .. import Mesh
from .. import regular_polygon
from .. import delaunay
from .. import spherical
from .. import polygon
from .. import hexagonal_grid
import numpy as np


def make_mesh(
    outer_radius,
    curvature_radius,
    n_hex_grid=10,
    ref="SphericalPixelCap",
    rot=0.0,
):
    mesh = Mesh.init()
    mesh["vertices"] = hexagonal_grid.make_vertices_xy(
        outer_radius=2.0 * outer_radius,
        ref="hex",
        n=n_hex_grid
    )

    for k in mesh["vertices"]:
        mesh["vertices"][k][2] = spherical.surface_height(
            x=mesh["vertices"][k][0],
            y=mesh["vertices"][k][1],
            curvature_radius=curvature_radius,
        )

    for k in mesh["vertices"]:
        mesh["vertex_normals"][k] = spherical.surface_normal(
            x=mesh["vertices"][k][0],
            y=mesh["vertices"][k][1],
            curvature_radius=curvature_radius,
        )

    all_grid_faces = delaunay.make_faces_xy(
        vertices=mesh["vertices"],
        ref=ref
    )

    for fkey in all_grid_faces:
        vkey_a = all_grid_faces[fkey]["vertices"][0]
        vkey_b = all_grid_faces[fkey]["vertices"][1]
        vkey_c = all_grid_faces[fkey]["vertices"][2]

        va = mesh["vertices"][vkey_a]
        vb = mesh["vertices"][vkey_b]
        vc = mesh["vertices"][vkey_c]

        ra = np.hypot(va[0], va[1])
        rb = np.hypot(vb[0], vb[1])
        rc = np.hypot(vc[0], vc[1])

        if ra <= outer_radius and rb <= outer_radius and rc <= outer_radius:
            mesh["faces"][fkey] = all_grid_faces[fkey]

            mesh["faces"][fkey]["vertex_normals"] = [
                vkey_a, vkey_b, vkey_c
            ]

    mesh["materials"][ref] = [ref]

    return Mesh.remove_unused_vertices_and_vertex_normals(mesh=mesh)
