from .. import Mesh
from .. import regular_polygon
from .. import delaunay
from .. import spherical
from .. import polygon
from .. import hexagonal_grid
import numpy as np


def make_round_mesh(
    outer_radius,
    curvature_radius,
    inner_radius=None,
    n_polygon=17,
    n_hex_grid=10,
    ref="SphericalCap",
    rot=0.0,
):
    outer_polygon = regular_polygon.make_vertices_xy(
        outer_radius=outer_radius,
        n=n_polygon,
        ref=ref + "/ring",
        rot=rot,
    )

    if inner_radius is not None:
        inner_polygon = regular_polygon.make_vertices_xy(
            outer_radius=inner_radius,
            n=n_polygon,
            ref=ref + "/inner_ring",
            rot=rot,
        )
    else:
        inner_polygon = None

    return _make_mesh(
        outer_polygon=outer_polygon,
        inner_polygon=inner_polygon,
        n_hex_grid=n_hex_grid,
        curvature_radius=curvature_radius,
        ref=ref
    )


def _make_mesh(
    outer_polygon,
    curvature_radius,
    inner_polygon=None,
    n_hex_grid=10,
    ref="SphericalCap"
):
    outer_limits = polygon.limits(outer_polygon)
    outer_radius_xy = np.max([
        np.max(np.abs(outer_limits[0])),
        np.max(np.abs(outer_limits[1]))
    ])

    hex_vertices = hexagonal_grid.make_vertices_xy(
        outer_radius=outer_radius_xy*1.5,
        n=n_hex_grid,
        ref=ref + "/Grid"
    )

    hex_vertices_valid = polygon.get_vertices_inside(
        vertices=hex_vertices,
        polygon=outer_polygon
    )

    if inner_polygon is not None:
        hex_vertices_valid = polygon.get_vertices_outside(
            vertices=hex_vertices_valid,
            polygon=inner_polygon
        )

    mesh = Mesh.init()

    for k in hex_vertices_valid:
        mesh["vertices"][k] = hex_vertices_valid[k]
    for k in outer_polygon:
        mesh["vertices"][k] = outer_polygon[k]
    if inner_polygon is not None:
        for k in inner_polygon:
            mesh["vertices"][k] = inner_polygon[k]

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

    faces = delaunay.make_faces_xy(vertices=mesh["vertices"], ref=ref)

    for fkey in faces:
        mesh["faces"][fkey] = {
            "vertices": faces[fkey]["vertices"],
            "vertex_normals": faces[fkey]["vertices"],
        }

    if inner_polygon is not None:
        mask_faces_in_inner = polygon.mask_face_inside(
            vertices=mesh["vertices"],
            faces=mesh["faces"],
            polygon=inner_polygon
        )
        fkeys_to_be_removed = []
        for idx, fkey in enumerate(mesh["faces"]):
            if mask_faces_in_inner[idx]:
                fkeys_to_be_removed.append(fkey)
        for fkey in fkeys_to_be_removed:
            mesh["faces"].pop(fkey)

    return mesh
