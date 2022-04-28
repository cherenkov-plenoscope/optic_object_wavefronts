from .. import Object
from .. import delaunay
from .. import Geometry
from . import disc
import copy
import numpy as np


def init(outer_radius, curvature_radius, fn=10, ref="SphericalCapHexagonal"):
    obj = Object.init()

    obj["vertices"] = Geometry.Grid.hexagonal.init_from_outer_radius(
        outer_radius=outer_radius, fn=fn, ref=ref + "/inner"
    )

    # elevate z-axis
    # --------------
    for vkey in obj["vertices"]:
        obj["vertices"][vkey][2] = Geometry.sphere.surface_height(
            x=obj["vertices"][vkey][0],
            y=obj["vertices"][vkey][1],
            curvature_radius=curvature_radius,
        )

    # vertex-normals
    # --------------
    for vkey in obj["vertices"]:
        vnkey = tuple(vkey)
        obj["vertex_normals"][vnkey] = Geometry.sphere.surface_normal(
            x=obj["vertices"][vkey][0],
            y=obj["vertices"][vkey][1],
            curvature_radius=curvature_radius,
        )

    faces = delaunay.make_faces_xy(vertices=obj["vertices"], ref=ref)

    for fkey in faces:
        obj["faces"][fkey] = {
            "vertices": faces[fkey]["vertices"],
            "vertex_normals": faces[fkey]["vertices"],
        }

    obj["materials"][ref] = [ref]
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

    for irotz, phi in enumerate(np.linspace(0, 2 * np.pi, 6, endpoint=False)):
        i_vertices = rotate_vertices_xy(vertices=obj["vertices"], phi=phi)

        i_combi_vertices = {}
        for fkey in i_vertices:
            if i_vertices[fkey][1] > 0.99 * inner_radius_hexagon:
                i_combi_vertices[fkey] = np.array(
                    [i_vertices[fkey][0], i_vertices[fkey][2], 0.0,]
                )

        i_faces = delaunay.make_faces_xy(
            vertices=i_combi_vertices, ref=ref + "_{:d}".format(irotz)
        )

        i_normal = np.array(
            [np.cos(-phi + rot_perp), np.sin(-phi + rot_perp), 0.0]
        )
        i_vnkey = (ref, irotz)

        obj["vertex_normals"][i_vnkey] = i_normal

        for fkey in i_faces:
            obj["faces"][fkey] = {
                "vertices": i_faces[fkey]["vertices"],
                "vertex_normals": [i_vnkey, i_vnkey, i_vnkey],
            }

    return obj
