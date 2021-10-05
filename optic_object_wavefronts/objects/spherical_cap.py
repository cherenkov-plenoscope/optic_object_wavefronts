from .. import Object
from .. import delaunay
from .. import geometry
from .. import polygon
import numpy as np


def init(
    outer_polygon,
    curvature_radius,
    inner_polygon=None,
    fn_hex_grid=10,
    ref="SphericalCap",
):
    outer_limits = polygon.limits(outer_polygon)
    outer_radius_xy = np.max(
        [np.max(np.abs(outer_limits[0])), np.max(np.abs(outer_limits[1]))]
    )

    hex_vertices = geometry.hexagonal_grid.make_vertices_xy(
        outer_radius=outer_radius_xy * 1.5, fn=fn_hex_grid, ref=ref + "/Grid"
    )

    hex_vertices_valid = polygon.get_vertices_inside(
        vertices=hex_vertices, polygon=outer_polygon
    )

    if inner_polygon is not None:
        hex_vertices_valid = polygon.get_vertices_outside(
            vertices=hex_vertices_valid, polygon=inner_polygon
        )

    obj = Object.init()

    for k in hex_vertices_valid:
        obj["vertices"][k] = hex_vertices_valid[k]
    for k in outer_polygon:
        obj["vertices"][k] = outer_polygon[k]
    if inner_polygon is not None:
        for k in inner_polygon:
            obj["vertices"][k] = inner_polygon[k]

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

    faces = delaunay.make_faces_xy(vertices=obj["vertices"], ref=ref)

    for fkey in faces:
        obj["faces"][fkey] = {
            "vertices": faces[fkey]["vertices"],
            "vertex_normals": faces[fkey]["vertices"],
        }

    if inner_polygon is not None:
        mask_faces_in_inner = polygon.mask_face_inside(
            vertices=obj["vertices"], faces=obj["faces"], polygon=inner_polygon
        )
        fkeys_to_be_removed = []
        for idx, fkey in enumerate(obj["faces"]):
            if mask_faces_in_inner[idx]:
                fkeys_to_be_removed.append(fkey)
        for fkey in fkeys_to_be_removed:
            obj["faces"].pop(fkey)

    obj["materials"][ref] = [ref]

    return obj
