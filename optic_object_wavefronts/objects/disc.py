from .. import Object
from .. import geometry
from .. import delaunay
import numpy as np


def init(
    outer_radius=1.0,
    fn=6,
    rot=0.0,
    ref="disc",
    prevent_many_faces_share_same_vertex=True,
):
    """
    Returns a disc-object.

    2D surface
    1 Material

    Parameters
    ----------
    outer_radius : float
            Outer radius of the regular polygon defining the disc.
    fn : int
            Number of vertices in outer regular polygon.
    rot : float
            Rotation in z of regular polygon.
    ref : str
            Key for the material.
    prevent_many_faces_share_same_vertex : bool
            Adds faces to reduce the number of faces sharing a single vertex.
            If False, only the vertices of the regular polygon will be used.
    """
    inner_radius = outer_radius * geometry.regular_polygon.inner_radius(fn=fn)

    obj = Object.init()
    obj["vertices"] = geometry.regular_polygon.make_vertices_xy(
        outer_radius=outer_radius, ref=ref + "/" + "outer_bound", fn=fn, rot=rot,
    )

    if prevent_many_faces_share_same_vertex:
        next_fn = int(np.round(fn / 3))
        next_radius = 0.9 * inner_radius
        v_inner_idx = 0
        while next_fn >= 6:
            inner_vertices = geometry.regular_polygon.make_vertices_xy(
                outer_radius=next_radius,
                ref=ref + "/" + "aux",
                fn=next_fn,
                rot=rot,
            )

            for inner_vkey in inner_vertices:
                _vkey = (ref + "/aux", v_inner_idx)
                obj["vertices"][_vkey] = inner_vertices[inner_vkey]
                v_inner_idx += 1

            next_radius = 0.9 * next_radius
            next_fn = int(np.round(next_fn / 3))

    vnkey = (ref, 0)
    obj["vertex_normals"][vnkey] = np.array([0.0, 0.0, 1.0])

    delfaces = delaunay.make_faces_xy(vertices=obj["vertices"], ref=ref)

    for fkey in delfaces:
        obj["faces"][fkey] = {
            "vertices": delfaces[fkey]["vertices"],
            "vertex_normals": [vnkey, vnkey, vnkey],
        }

    obj["materials"][ref] = [ref]

    return obj
