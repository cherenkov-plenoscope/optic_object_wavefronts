from .. import Object
from .. import delaunay
from .. import geometry
from .. import polygon
import numpy as np


def make_obj(
    outer_radius,
    curvature_radius,
    n_hex_grid=10,
    ref="SphericalPixelCap",
    rot=0.0,
):
    obj = Object.init()
    obj["vertices"] = geometry.hexagonal_grid.make_vertices_xy(
        outer_radius=2.0 * outer_radius,
        ref="hex",
        n=n_hex_grid
    )

    for k in obj["vertices"]:
        obj["vertices"][k][2] = geometry.sphere.surface_height(
            x=obj["vertices"][k][0],
            y=obj["vertices"][k][1],
            curvature_radius=curvature_radius,
        )

    for k in obj["vertices"]:
        obj["vertex_normals"][k] = geometry.sphere.surface_normal(
            x=obj["vertices"][k][0],
            y=obj["vertices"][k][1],
            curvature_radius=curvature_radius,
        )

    all_grid_faces = delaunay.make_faces_xy(
        vertices=obj["vertices"],
        ref=ref
    )

    for fkey in all_grid_faces:
        vkey_a = all_grid_faces[fkey]["vertices"][0]
        vkey_b = all_grid_faces[fkey]["vertices"][1]
        vkey_c = all_grid_faces[fkey]["vertices"][2]

        va = obj["vertices"][vkey_a]
        vb = obj["vertices"][vkey_b]
        vc = obj["vertices"][vkey_c]

        ra = np.hypot(va[0], va[1])
        rb = np.hypot(vb[0], vb[1])
        rc = np.hypot(vc[0], vc[1])

        if ra <= outer_radius and rb <= outer_radius and rc <= outer_radius:
            obj["faces"][fkey] = all_grid_faces[fkey]

            obj["faces"][fkey]["vertex_normals"] = [
                vkey_a, vkey_b, vkey_c
            ]

    obj["materials"][ref] = [ref]

    return Object.remove_unused_vertices_and_vertex_normals(obj=obj)
