from .. import Object
from .. import delaunay
from .. import Geometry
from .. import Polygon
import numpy as np
import collections


def init(
    outer_radius, curvature_radius, fn_hex_grid=10, ref="SphericalPixelCap",
):
    obj = Object.init()
    obj["vertices"] = Geometry.Grid.Hexagonal.init_from_outer_radius(
        outer_radius=2.0 * outer_radius, ref="hex", fn=fn_hex_grid
    )

    for k in obj["vertices"]:
        obj["vertices"][k][2] = Geometry.Sphere.surface_height(
            x=obj["vertices"][k][0],
            y=obj["vertices"][k][1],
            curvature_radius=curvature_radius,
        )

    for k in obj["vertices"]:
        obj["vertex_normals"][k] = Geometry.Sphere.surface_normal(
            x=obj["vertices"][k][0],
            y=obj["vertices"][k][1],
            curvature_radius=curvature_radius,
        )

    mtl_key = ref
    obj["materials"][mtl_key] = collections.OrderedDict()

    all_grid_faces = delaunay.make_faces_xy(vertices=obj["vertices"], ref=ref)

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
            obj["materials"][mtl_key][fkey] = all_grid_faces[fkey]
            obj["materials"][mtl_key][fkey]["vertex_normals"] = [
                vkey_a,
                vkey_b,
                vkey_c,
            ]

    return Object.remove_unused_vertices_and_vertex_normals(obj=obj)
