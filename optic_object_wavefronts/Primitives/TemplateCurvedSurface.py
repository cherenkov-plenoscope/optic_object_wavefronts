from .. import Object
from .. import delaunay
from .. import Geometry
from .. import polygon
import numpy as np
import os
import collections


def init(
    outer_polygon,
    curvature_config,
    curvature_height_function,
    curvature_surface_normal_function,
    inner_polygon=None,
    fn_hex_grid=10,
    ref="CurvedSurface",
):
    """
    Returns an object that describes a curved 2d surface. The user provides
    f unctions which control the curvature's height and surface-normal.

    outer_polygon : 2D-polygon-dict
            The outer bound of the surface.
    curvature_config : dict
            The config of the curvature. This is fed to the height-, and
            surface-normal-function.
    curvature_height_function : function
            Takes arguments x, y, and **curvature_config.
            Is expected to return the height z.
    curvature_surface_normal_function : function
            Takes arguments x, y, and **curvature_config.
            Is expected to return the surface-normal.
    outer_polygon : 2D-polygon-dict
            The inner bound of the surface.
    fn_hex_grid : int
            Density of hexagonal grid in the surface.
    ref : string
            The name of the surface.
    """
    outer_limits = polygon.limits(outer_polygon)
    outer_radius_xy = np.max(
        [np.max(np.abs(outer_limits[0])), np.max(np.abs(outer_limits[1]))]
    )

    hex_vertices = Geometry.Grid.Hexagonal.init_from_outer_radius(
        outer_radius=outer_radius_xy * 1.5,
        fn=fn_hex_grid,
        ref=os.path.join(ref, "grid"),
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
        obj["vertices"][k][2] = curvature_height_function(
            x=obj["vertices"][k][0],
            y=obj["vertices"][k][1],
            **curvature_config,
        )

    for k in obj["vertices"]:
        obj["vertex_normals"][k] = curvature_surface_normal_function(
            x=obj["vertices"][k][0],
            y=obj["vertices"][k][1],
            **curvature_config,
        )

    faces = delaunay.make_faces_xy(vertices=obj["vertices"], ref=ref)

    obj["materials"][ref] = collections.OrderedDict()

    mtl_key = ref
    for fkey in faces:
        obj["materials"][mtl_key][fkey] = {
            "vertices": faces[fkey]["vertices"],
            "vertex_normals": faces[fkey]["vertices"],
        }

    if inner_polygon is not None:
        mask_faces_in_inner = polygon.mask_face_inside(
            vertices=obj["vertices"],
            faces=obj["materials"][mtl_key],
            polygon=inner_polygon,
        )
        fkeys_to_be_removed = []
        for idx, fkey in enumerate(obj["materials"][mtl_key]):
            if mask_faces_in_inner[idx]:
                fkeys_to_be_removed.append(fkey)
        for fkey in fkeys_to_be_removed:
            obj["materials"][mtl_key].pop(fkey)

    return obj
