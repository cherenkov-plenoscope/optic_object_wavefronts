from .. import Object
from .. import delaunay
from .. import geometry
from . import disc
import copy
import numpy as np


def init(
    outer_radius,
    curvature_radius,
    n=10,
    ref="SphericalCapHexagonal"
):
    obj = Object.init()

    obj["vertices"] = geometry.hexagonal_grid.make_vertices_xy(
        outer_radius=outer_radius,
        n=n,
        ref=ref + "/inner"
    )

    # elevate z-axis
    # --------------
    for vkey in obj["vertices"]:
        obj["vertices"][vkey][2] = geometry.sphere.surface_height(
            x=obj["vertices"][vkey][0],
            y=obj["vertices"][vkey][1],
            curvature_radius=curvature_radius,
        )

    # vertex-normals
    # --------------
    for vkey in obj["vertices"]:
        vnkey = tuple(vkey)
        obj["vertex_normals"][vnkey] = geometry.sphere.surface_normal(
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
    inner_radius_hexagon = outer_radius * geometry.regular_polygon.inner_radius(n=6)
    inner_radius_threshold = inner_radius_hexagon - margin_width_on_edge
    rot_perp = np.pi / 2.0

    for irotz, phi in enumerate(np.linspace(0, 2*np.pi, 6, endpoint=False)):
        i_vertices = rotate_vertices_xy(vertices=obj["vertices"], phi=phi)

        i_combi_vertices = {}
        for fkey in i_vertices:
            if i_vertices[fkey][1] > 0.99 * inner_radius_hexagon:
                i_combi_vertices[fkey] = np.array([
                    i_vertices[fkey][0],
                    i_vertices[fkey][2],
                    0.0,
                ])

        i_faces = delaunay.make_faces_xy(
            vertices=i_combi_vertices,
            ref=ref + "_{:d}".format(irotz)
        )

        i_normal = np.array([
            np.cos(-phi + rot_perp),
            np.sin(-phi + rot_perp),
            0.0
        ])
        i_vnkey = (ref, irotz)

        obj["vertex_normals"][i_vnkey] = i_normal

        for fkey in i_faces:
            obj["faces"][fkey] = {
                "vertices": i_faces[fkey]["vertices"],
                "vertex_normals": [i_vnkey, i_vnkey, i_vnkey],
            }

    return obj


def make_front_spherical_back_plane_obj(
    outer_radius,
    curvature_radius,
    width,
    n=10,
    ref="SphericalPlaneHexagonalBody"
):
    front_obj = make_obj(
        outer_radius=outer_radius,
        curvature_radius=curvature_radius,
        n=n,
        ref=ref + "/front"
    )

    back_obj = disc.make_obj(
        outer_radius=outer_radius,
        n=6,
        ref=ref + "/back",
        rot=0.0,
    )

    center_of_curvature = np.array([0.0, 0.0, curvature_radius])

    back_obj = Object.translate(back_obj, [0.0, 0.0, -width])
    for vnkey in back_obj["vertex_normals"]:
        back_obj["vertex_normals"][vnkey] = np.array([0.0, 0.0, -1.0])

    obj = Object.merge(front_obj, back_obj)

    hexagonal_grid_spacing = outer_radius / n

    obj = weave_hexagon_edges(
        obj=obj,
        outer_radius=outer_radius,
        margin_width_on_edge=0.1 * hexagonal_grid_spacing,
        ref=ref + "/side",
    )

    # remove /side faces inside of curvature-sphere
    side_fkeys = []
    for fkey in obj["faces"]:
        if str.find(fkey[0], ref + "/side") >= 0:
            side_fkeys.append(fkey)

    for fkey in side_fkeys:
        va_key = obj["faces"][fkey]["vertices"][0]
        vb_key = obj["faces"][fkey]["vertices"][1]
        vc_key = obj["faces"][fkey]["vertices"][2]

        va = obj["vertices"][va_key]
        vb = obj["vertices"][vb_key]
        vc = obj["vertices"][vc_key]

        mid_ab = 0.5 * (va + vb)
        mid_bc = 0.5 * (vb + vc)
        mid_ca = 0.5 * (vc + va)

        r_mid_ab = np.linalg.norm(mid_ab - center_of_curvature)
        r_mid_bc = np.linalg.norm(mid_bc - center_of_curvature)
        r_mid_ca = np.linalg.norm(mid_ca - center_of_curvature)

        mid_ab_inside = r_mid_ab <= curvature_radius
        mid_bc_inside = r_mid_bc <= curvature_radius
        mid_ca_inside = r_mid_ca <= curvature_radius

        if np.sum([mid_ab_inside, mid_bc_inside, mid_ca_inside]) > 1:
            obj["faces"].pop(fkey)

    obj["materials"] = {}
    obj["materials"][ref+"_front"] = [ref + "/front"]
    obj["materials"][ref+"_back"] = [ref + "/back"]
    obj["materials"][ref+"_side"] = [ref + "/side"]

    return obj
