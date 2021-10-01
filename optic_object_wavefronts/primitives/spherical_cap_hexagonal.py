from .. import Mesh
from .. import delaunay
from .. import geometry
from . import disc
from .. import regular_polygon
from .. import hexagonal_grid
import copy
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
        mesh["vertices"][vkey][2] = geometry.sphere.surface_height(
            x=mesh["vertices"][vkey][0],
            y=mesh["vertices"][vkey][1],
            curvature_radius=curvature_radius,
        )

    # vertex-normals
    # --------------
    for vkey in mesh["vertices"]:
        vnkey = tuple(vkey)
        mesh["vertex_normals"][vnkey] = geometry.sphere.surface_normal(
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


def weave_hexagon_edges(mesh, outer_radius, margin_width_on_edge, ref):
    assert outer_radius >= 0
    assert margin_width_on_edge >= 0
    inner_radius_hexagon = outer_radius * regular_polygon.inner_radius(n=6)
    inner_radius_threshold = inner_radius_hexagon - margin_width_on_edge
    rot_perp = np.pi / 2.0

    for irotz, phi in enumerate(np.linspace(0, 2*np.pi, 6, endpoint=False)):
        i_vertices = rotate_vertices_xy(vertices=mesh["vertices"], phi=phi)

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

        mesh["vertex_normals"][i_vnkey] = i_normal

        for fkey in i_faces:
            mesh["faces"][fkey] = {
                "vertices": i_faces[fkey]["vertices"],
                "vertex_normals": [i_vnkey, i_vnkey, i_vnkey],
            }

    return mesh


def make_front_spherical_back_plane_mesh(
    outer_radius,
    curvature_radius,
    width,
    n=10,
    ref="SphericalPlaneHexagonalBody"
):
    front_mesh = make_mesh(
        outer_radius=outer_radius,
        curvature_radius=curvature_radius,
        n=n,
        ref=ref + "/front"
    )

    back_mesh = disc.make_mesh(
        outer_radius=outer_radius,
        n=6,
        ref=ref + "/back",
        rot=0.0,
    )

    center_of_curvature = np.array([0.0, 0.0, curvature_radius])

    back_mesh = Mesh.translate(back_mesh, [0.0, 0.0, -width])
    for vnkey in back_mesh["vertex_normals"]:
        back_mesh["vertex_normals"][vnkey] = np.array([0.0, 0.0, -1.0])

    mesh = Mesh.merge(front_mesh, back_mesh)

    hexagonal_grid_spacing = outer_radius / n

    mesh = weave_hexagon_edges(
        mesh=mesh,
        outer_radius=outer_radius,
        margin_width_on_edge=0.1 * hexagonal_grid_spacing,
        ref=ref + "/side",
    )

    # remove /side faces inside of curvature-sphere
    side_fkeys = []
    for fkey in mesh["faces"]:
        if str.find(fkey[0], ref + "/side") >= 0:
            side_fkeys.append(fkey)

    for fkey in side_fkeys:
        va_key = mesh["faces"][fkey]["vertices"][0]
        vb_key = mesh["faces"][fkey]["vertices"][1]
        vc_key = mesh["faces"][fkey]["vertices"][2]

        va = mesh["vertices"][va_key]
        vb = mesh["vertices"][vb_key]
        vc = mesh["vertices"][vc_key]

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
            mesh["faces"].pop(fkey)

    mesh["materials"] = {}
    mesh["materials"][ref+"_front"] = [ref + "/front"]
    mesh["materials"][ref+"_back"] = [ref + "/back"]
    mesh["materials"][ref+"_side"] = [ref + "/side"]

    return mesh
