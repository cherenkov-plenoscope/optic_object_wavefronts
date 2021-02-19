from .. import Mesh
from .. import delaunay
from .. import spherical
from .. import hexagonal_grid
import numpy as np


def make_mesh(
    outer_radius,
    curvature_radius,
    n=10,
    ref="SphericalCapHexagonal"
):
    mesh = Mesh.init()

    mesh["vertices"] = hexagonal_grid.make_vertices_xy(
        outer_radius=outer_radius,
        n=n,
        ref=ref + "/inner"
    )

    # elevate z-axis
    # --------------
    for vkey in mesh["vertices"]:
        mesh["vertices"][vkey][2] = spherical.surface_height(
            x=mesh["vertices"][vkey][0],
            y=mesh["vertices"][vkey][1],
            curvature_radius=curvature_radius,
        )

    # vertex-normals
    # --------------
    for vkey in mesh["vertices"]:
        vnkey = tuple(vkey)
        mesh["vertex_normals"][vnkey] = spherical.surface_normal(
            x=mesh["vertices"][vkey][0],
            y=mesh["vertices"][vkey][1],
            curvature_radius=curvature_radius,
        )

    faces = delaunay.make_faces_xy(vertices=mesh["vertices"], ref=ref)

    for fkey in faces:
        mesh["faces"][fkey] = {
            "vertices": faces[fkey]["vertices"],
            "vertex_normals": faces[fkey]["vertices"],
        }

    mesh["materials"][ref] = [ref]
    return mesh
