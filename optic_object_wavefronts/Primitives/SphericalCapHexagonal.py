from .. import Object
from .. import Delaunay
from .. import Geometry
from . import Disc
import copy
import numpy as np
import os
import collections


def init(outer_radius, curvature_radius, fn=10, ref="SphericalCapHexagonal"):
    obj = Object.init()

    obj["vertices"] = Geometry.Grid.Hexagonal.init_from_outer_radius(
        outer_radius=outer_radius, fn=fn, ref=os.path.join(ref, "inner")
    )

    # elevate z-axis
    # --------------
    for vkey in obj["vertices"]:
        obj["vertices"][vkey][2] = Geometry.Sphere.surface_height(
            x=obj["vertices"][vkey][0],
            y=obj["vertices"][vkey][1],
            curvature_radius=curvature_radius,
        )

    # vertex-normals
    # --------------
    for vkey in obj["vertices"]:
        vnkey = str(vkey)
        obj["vertex_normals"][vnkey] = Geometry.Sphere.surface_normal(
            x=obj["vertices"][vkey][0],
            y=obj["vertices"][vkey][1],
            curvature_radius=curvature_radius,
        )

    faces = Delaunay.make_faces_xy(vertices=obj["vertices"], ref="")

    mtl_key = ref
    obj["materials"][mtl_key] = collections.OrderedDict()
    for fkey in faces:
        obj["materials"][mtl_key][fkey] = {
            "vertices": faces[fkey]["vertices"],
            "vertex_normals": faces[fkey]["vertices"],
        }

    return obj


def rotate_vertices_xy(vertices, phi):
    cosp = np.cos(phi)
    sinp = np.sin(phi)
    vertices_out = copy.deepcopy(vertices)
    for vkey in vertices_out:
        x = vertices_out[vkey][0]
        y = vertices_out[vkey][1]
        nx = cosp * x - sinp * y
        ny = sinp * x + cosp * y
        vertices_out[vkey][0] = nx
        vertices_out[vkey][1] = ny
    return vertices_out


def weave_hexagon_edges(obj, outer_radius, margin_width_on_edge, ref):
    assert outer_radius >= 0
    assert margin_width_on_edge >= 0
    inner_radius_hexagon = outer_radius * Geometry.RegularPolygon.inner_radius(
        fn=6
    )
    inner_radius_threshold = inner_radius_hexagon - margin_width_on_edge
    rot_perp = np.pi / 2.0

    mtl_key = ref
    obj["materials"][mtl_key] = collections.OrderedDict()

    for irotz, phi in enumerate(np.linspace(0, 2 * np.pi, 6, endpoint=False)):
        i_vertices = rotate_vertices_xy(vertices=obj["vertices"], phi=phi)

        i_combi_vertices = {}
        for fkey in i_vertices:
            if i_vertices[fkey][1] > 0.99 * inner_radius_hexagon:
                i_combi_vertices[fkey] = np.array(
                    [i_vertices[fkey][0], i_vertices[fkey][2], 0.0,]
                )

        i_faces = Delaunay.make_faces_xy(
            vertices=i_combi_vertices, ref=ref + "{:d}".format(irotz)
        )

        i_normal = np.array(
            [np.cos(-phi + rot_perp), np.sin(-phi + rot_perp), 0.0]
        )
        i_vnkey = os.path.join(ref, "{:06d}".format(irotz))

        obj["vertex_normals"][i_vnkey] = i_normal

        for fkey in i_faces:
            obj["materials"][mtl_key][fkey] = {
                "vertices": i_faces[fkey]["vertices"],
                "vertex_normals": [i_vnkey, i_vnkey, i_vnkey],
            }

    return obj
