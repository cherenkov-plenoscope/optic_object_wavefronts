from . import Mesh
from . import regular_polygon
from . import delaunay
from . import spherical

import numpy as np
from . import geometry as optical_geometry

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
            curvature_radius=curvature_radius
        )

    # vertex-normals
    # --------------
    for vkey in m["vertices"]:
        vnkey = (vkey[0], vkey[1], "c")
        m["vertex_normals"][vnkey] = spherical.surface_normal(
            x=m["vertices"][vkey][0],
            y=m["vertices"][vkey][1],
            curvature_radius=curvature_radius)

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


def make_disc_mesh(ref="disc", radius=1.0, n=6, phi_off=0.0):
    inner_radius = radius * regular_polygon.inner_radius(n=n)

    mesh = Mesh.init()
    mesh["vertices"] = regular_polygon.make_vertices_xy(
        outer_radius=1.0,
        ref=ref + "/" + "ring", n=n, rot=phi_off
    )

    for vkey in mesh["vertices"]:
        mesh["vertices"][vkey] = radius * mesh["vertices"][vkey]

    next_n = int(np.round(n / 3))
    next_radius = 0.8 * inner_radius
    v_inner_idx = 0
    while next_n >= 6:
        inner_vertices = regular_polygon.make_vertices_xy(
            outer_radius=1.0,
            ref=ref + "/" + "inner", n=next_n, rot=phi_off
        )

        for inner_vkey in inner_vertices:
            _vkey = (ref + "/inner", v_inner_idx)
            mesh["vertices"][_vkey] = next_radius * inner_vertices[inner_vkey]
            v_inner_idx += 1

        next_radius = 0.8 * next_radius
        next_n = int(np.round(next_n / 3))

    vnkey = (ref, 0)
    mesh["vertex_normals"][vnkey] = np.array([0.0, 0.0, 1.0])

    delfaces = delaunay.make_faces_xy(vertices=mesh["vertices"], ref=ref)

    for fkey in delfaces:
        mesh["faces"][fkey] = {
            "vertices": delfaces[fkey]["vertices"],
            "vertex_normals": [vnkey, vnkey, vnkey],
        }

    return mesh


def make_cylinder_mesh(
    ref="cylinder", radius=1.0, length=1.0, n=6, phi_off=0.0
):
    top = make_disc_mesh(
        ref="cylinder/top", radius=radius, n=n, phi_off=phi_off
    )
    bot = make_disc_mesh(
        ref="cylinder/bot",
        radius=radius,
        n=n,
        phi_off=(2 * np.pi) / (2 * n) + phi_off,
    )

    mesh = Mesh.init()

    for vkey in top["vertices"]:
        tmp_v = np.array(top["vertices"][vkey])
        tmp_v[2] = float(length)
        mesh["vertices"][vkey] = tmp_v
    for fkey in top["faces"]:
        mesh["faces"][fkey] = top["faces"][fkey]
    for vnkey in top["vertex_normals"]:
        mesh["vertex_normals"][vnkey] = [0, 0, 1]

    for vkey in bot["vertices"]:
        mesh["vertices"][vkey] = bot["vertices"][vkey]
    for fkey in bot["faces"]:
        mesh["faces"][fkey] = bot["faces"][fkey]
    for vnkey in bot["vertex_normals"]:
        mesh["vertex_normals"][vnkey] = [0, 0, -1]

    for ni in range(n):
        side_fkey = ("cylinder/side_ttb", ni)
        n_a = int(ni)
        n_b = int(n_a + 1)
        if n_b == n:
            n_b = 0
        n_c = int(ni)
        va = np.array(mesh["vertices"][("cylinder/top/ring", n_a)])
        vb = np.array(mesh["vertices"][("cylinder/top/ring", n_b)])
        vc = np.array(mesh["vertices"][("cylinder/bot/ring", n_c)])
        va[2] = 0.0
        vb[2] = 0.0
        vc[2] = 0.0
        if ("cylinder/side/top", n_a) not in mesh["vertex_normals"]:
            mesh["vertex_normals"][
                ("cylinder/side/top", n_a)
            ] = va / np.linalg.norm(va)

        if ("cylinder/side/top", n_b) not in mesh["vertex_normals"]:
            mesh["vertex_normals"][
                ("cylinder/side/top", n_b)
            ] = vb / np.linalg.norm(vb)

        if ("cylinder/side/bot", n_c) not in mesh["vertex_normals"]:
            mesh["vertex_normals"][
                ("cylinder/side/bot", n_c)
            ] = vc / np.linalg.norm(vc)

        mesh["faces"][side_fkey] = {
            "vertices": [
                ("cylinder/top/ring", n_a),
                ("cylinder/top/ring", n_b),
                ("cylinder/bot/ring", n_c),
            ],
            "vertex_normals": [
                ("cylinder/side/top", n_a),
                ("cylinder/side/top", n_b),
                ("cylinder/side/bot", n_c),
            ],
        }

    for ni in range(n):
        side_fkey = ("cylinder/side_bbt", ni)
        n_a = int(ni)
        n_b = int(n_a + 1)
        if n_b == n:
            n_b = 0
        n_c = int(ni + 1)
        if n_c == n:
            n_c = 0
        va = np.array(mesh["vertices"][("cylinder/bot/ring", n_a)])
        vb = np.array(mesh["vertices"][("cylinder/bot/ring", n_b)])
        vc = np.array(mesh["vertices"][("cylinder/top/ring", n_c)])
        va[2] = 0.0
        vb[2] = 0.0
        vc[2] = 0.0
        if ("cylinder/side/bot", n_a) not in mesh["vertex_normals"]:
            mesh["vertex_normals"][
                ("cylinder/side/bot", n_a)
            ] = va / np.linalg.norm(va)

        if ("cylinder/side/bot", n_b) not in mesh["vertex_normals"]:
            mesh["vertex_normals"][
                ("cylinder/side/bot", n_b)
            ] = vb / np.linalg.norm(vb)

        if ("cylinder/side/top", n_c) not in mesh["vertex_normals"]:
            mesh["vertex_normals"][
                ("cylinder/side/top", n_c)
            ] = vc / np.linalg.norm(vc)

        mesh["faces"][side_fkey] = {
            "vertices": [
                ("cylinder/bot/ring", n_a),
                ("cylinder/bot/ring", n_b),
                ("cylinder/top/ring", n_c),
            ],
            "vertex_normals": [
                ("cylinder/side/bot", n_a),
                ("cylinder/side/bot", n_b),
                ("cylinder/side/top", n_c),
            ],
        }

    return mesh
