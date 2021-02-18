from . import Mesh
from . import regular_polygon
from . import delaunay
from . import spherical

import numpy as np

HEXA = np.array([1.0, 0.0, 0.0])
HEXB = np.array([0.5, np.sqrt(3.0) / 2.0, 0.0])


def make_hexagonal_mesh_in_xy_plane(radial_steps):
    # vertices
    # ========
    n = radial_steps
    mesh = Mesh.init()
    for dA in np.arange(-n, n + 1, 1):
        for dB in np.arange(-n, n + 1, 1):

            bound_upper = -dA + n
            bound_lower = -dA - n
            if dB <= bound_upper and dB >= bound_lower:
                mesh["vertices"][(dA, dB)] = dA * HEXA + dB * HEXB

    # faces
    # =====
    for dA in np.arange(-n, n + 1, 1):
        for dB in np.arange(-n, n + 1, 1):

            # top face
            # --------
            top_face_verts = [(dA, dB), (dA + 1, dB), (dA, dB + 1)]

            all_faces_in_mesh = True
            for top_face_vert in top_face_verts:
                if top_face_vert not in mesh["vertices"]:
                    all_faces_in_mesh = False

            if all_faces_in_mesh:
                mesh["faces"][(dA, dB, 1)] = {"vertices": list(top_face_verts)}
            # bottom face
            # -----------
            bottom_face_verts = [(dA, dB), (dA + 1, dB), (dA + 1, dB - 1)]

            all_faces_in_mesh = True
            for bottom_face_vert in bottom_face_verts:
                if bottom_face_vert not in mesh["vertices"]:
                    all_faces_in_mesh = False

            if all_faces_in_mesh:
                mesh["faces"][(dA, dB, -1)] = {
                    "vertices": list(bottom_face_verts)
                }

    return mesh


def make_spherical_hex_cap(outer_hex_radius, curvature_radius, num_steps=10):
    # flat 2d-mesh
    m = make_hexagonal_mesh_in_xy_plane(radial_steps=num_steps)

    # scale
    for vkey in m["vertices"]:
        m["vertices"][vkey] *= 2.0 * outer_hex_radius * 1.0 / num_steps

    # elevate z-axis
    for vkey in m["vertices"]:
        m["vertices"][vkey][2] = spherical.surface_height(
            x=m["vertices"][vkey][0],
            y=m["vertices"][vkey][1],
            curvature_radius=curvature_radius,
        )

    # vertex-normals
    # --------------
    for vkey in m["vertices"]:
        vnkey = (vkey[0], vkey[1], "c")
        m["vertex_normals"][vnkey] = spherical.surface_normal(
            x=m["vertices"][vkey][0],
            y=m["vertices"][vkey][1],
            curvature_radius=curvature_radius,
        )

    for fkey in m["faces"]:
        v0_key = m["faces"][fkey]["vertices"][0]
        v1_key = m["faces"][fkey]["vertices"][1]
        v2_key = m["faces"][fkey]["vertices"][2]
        m["faces"][fkey]["vertex_normals"] = [
            (v0_key[0], v0_key[1], "c"),
            (v1_key[0], v1_key[1], "c"),
            (v2_key[0], v2_key[1], "c"),
        ]
    return m
