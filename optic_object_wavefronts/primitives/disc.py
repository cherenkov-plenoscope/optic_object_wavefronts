from .. import Mesh
from .. import regular_polygon
from .. import delaunay
import numpy as np


def make_mesh(outer_radius=1.0, n=6, rot=0.0, ref="disc"):
    inner_radius = outer_radius * regular_polygon.inner_radius(n=n)

    mesh = Mesh.init()
    mesh["vertices"] = regular_polygon.make_vertices_xy(
        outer_radius=outer_radius,
        ref=ref + "/" + "ring",
        n=n,
        rot=rot
    )

    next_n = int(np.round(n / 3))
    next_radius = 0.9 * inner_radius
    v_inner_idx = 0
    while next_n >= 6:
        inner_vertices = regular_polygon.make_vertices_xy(
            outer_radius=next_radius,
            ref=ref + "/" + "inner",
            n=next_n,
            rot=rot
        )

        for inner_vkey in inner_vertices:
            _vkey = (ref + "/inner", v_inner_idx)
            mesh["vertices"][_vkey] = inner_vertices[inner_vkey]
            v_inner_idx += 1

        next_radius = 0.9 * next_radius
        next_n = int(np.round(next_n / 3))

    vnkey = (ref, 0)
    mesh["vertex_normals"][vnkey] = np.array([0.0, 0.0, 1.0])

    delfaces = delaunay.make_faces_xy(vertices=mesh["vertices"], ref=ref)

    for fkey in delfaces:
        mesh["faces"][fkey] = {
            "vertices": delfaces[fkey]["vertices"],
            "vertex_normals": [vnkey, vnkey, vnkey],
        }

    return mesh
