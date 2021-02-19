from .. import Mesh
from . import disc
import numpy as np


def _find_keys(dic, key):
    out = []
    for k in dic:
        if key in k:
            out.append(k)
    return out


def weave_cylinder_faces(
    mesh,
    ref,
    vkey_lower,
    vkey_upper
):

    num_v_lower = len(_find_keys(mesh["vertices"], vkey_lower))
    num_v_upper = len(_find_keys(mesh["vertices"], vkey_upper))
    assert num_v_lower == num_v_upper
    n = num_v_upper

    for ni in range(n):
        n_a = int(ni)
        n_b = int(n_a + 1)
        if n_b == n:
            n_b = 0
        n_c = int(ni)
        va = np.array(mesh["vertices"][(vkey_upper, n_a)])
        vb = np.array(mesh["vertices"][(vkey_upper, n_b)])
        vc = np.array(mesh["vertices"][(vkey_lower, n_c)])
        va[2] = 0.0
        vb[2] = 0.0
        vc[2] = 0.0
        if (ref + "/side/top", n_a) not in mesh["vertex_normals"]:
            mesh["vertex_normals"][
                (ref + "/side/top", n_a)
            ] = va / np.linalg.norm(va)

        if (ref + "/side/top", n_b) not in mesh["vertex_normals"]:
            mesh["vertex_normals"][
                (ref + "/side/top", n_b)
            ] = vb / np.linalg.norm(vb)

        if (ref + "/side/bot", n_c) not in mesh["vertex_normals"]:
            mesh["vertex_normals"][
                (ref + "/side/bot", n_c)
            ] = vc / np.linalg.norm(vc)

        side_fkey = (ref + "/side_ttb", ni)
        mesh["faces"][side_fkey] = {
            "vertices": [
                (vkey_upper, n_a),
                (vkey_upper, n_b),
                (vkey_lower, n_c),
            ],
            "vertex_normals": [
                (ref + "/side/top", n_a),
                (ref + "/side/top", n_b),
                (ref + "/side/bot", n_c),
            ],
        }

    for ni in range(n):
        n_a = int(ni)
        n_b = int(n_a + 1)
        if n_b == n:
            n_b = 0
        n_c = int(ni + 1)
        if n_c == n:
            n_c = 0
        va = np.array(mesh["vertices"][(vkey_lower, n_a)])
        vb = np.array(mesh["vertices"][(vkey_lower, n_b)])
        vc = np.array(mesh["vertices"][(vkey_upper, n_c)])
        va[2] = 0.0
        vb[2] = 0.0
        vc[2] = 0.0
        if (ref + "/side/bot", n_a) not in mesh["vertex_normals"]:
            mesh["vertex_normals"][
                (ref + "/side/bot", n_a)
            ] = va / np.linalg.norm(va)

        if (ref + "/side/bot", n_b) not in mesh["vertex_normals"]:
            mesh["vertex_normals"][
                (ref + "/side/bot", n_b)
            ] = vb / np.linalg.norm(vb)

        if (ref + "/side/top", n_c) not in mesh["vertex_normals"]:
            mesh["vertex_normals"][
                (ref + "/side/top", n_c)
            ] = vc / np.linalg.norm(vc)

        side_fkey = (ref + "/side_bbt", ni)
        mesh["faces"][side_fkey] = {
            "vertices": [
                (vkey_lower, n_a),
                (vkey_lower, n_b),
                (vkey_upper, n_c),
            ],
            "vertex_normals": [
                (ref + "/side/bot", n_a),
                (ref + "/side/bot", n_b),
                (ref + "/side/top", n_c),
            ],
        }

    return mesh


def make_mesh(
    outer_radius=1.0, length=1.0, n=6, rot=0.0, ref="cylinder"
):
    top = disc.make_mesh(
        outer_radius=outer_radius,
        ref="cylinder/top",
        n=n,
        rot=rot
    )
    bot = disc.make_mesh(
        outer_radius=outer_radius,
        ref="cylinder/bot",
        n=n,
        rot=(2 * np.pi) / (2 * n) + rot,
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

    mesh = weave_cylinder_faces(mesh=mesh,
        vkey_lower="cylinder/bot/ring",
        vkey_upper="cylinder/top/ring"
    )

    return mesh
