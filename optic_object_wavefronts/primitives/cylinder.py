from .. import Mesh
from . import disc
import numpy as np


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
