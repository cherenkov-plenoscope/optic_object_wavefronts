import numpy as np
from .. import Mesh
from . import cylinder
from . import spherical_cap


def make_mesh(
    outer_radius,
    curvature_radius_top,
    curvature_radius_bot,
    offset,
    n_polygon,
    n_hex_grid,
    rot,
    ref,
    inner_radius=None
):
    top = spherical_cap.make_round_mesh(
        outer_radius=outer_radius,
        inner_radius=inner_radius,
        curvature_radius=-1.0 * curvature_radius_top,
        ref=ref + "/top",
        n_polygon=n_polygon,
        n_hex_grid=n_hex_grid,
        rot=rot
    )
    bot = spherical_cap.make_round_mesh(
        outer_radius=outer_radius,
        inner_radius=inner_radius,
        curvature_radius=-1.0 * curvature_radius_bot,
        ref=ref + "/bot",
        n_polygon=n_polygon,
        n_hex_grid=n_hex_grid,
        rot=(2 * np.pi) / (2 * n_polygon) + rot,
    )

    mesh = Mesh.init()

    for vkey in top["vertices"]:
        tmp_v = np.array(top["vertices"][vkey])
        # tmp_v[2] = tmp_v[2] + 0.5 * float(offset)
        mesh["vertices"][vkey] = tmp_v
    for fkey in top["faces"]:
        mesh["faces"][fkey] = top["faces"][fkey]
    for vnkey in top["vertex_normals"]:
        mesh["vertex_normals"][vnkey] = +1.0 * top["vertex_normals"][vnkey]

    for vkey in bot["vertices"]:
        tmp_v = np.array(bot["vertices"][vkey])
        tmp_v[2] = tmp_v[2] - float(offset)
        mesh["vertices"][vkey] = tmp_v
    for fkey in bot["faces"]:
        mesh["faces"][fkey] = bot["faces"][fkey]
    for vnkey in bot["vertex_normals"]:
        mesh["vertex_normals"][vnkey] = -1.0 * bot["vertex_normals"][vnkey]

    mesh = cylinder.weave_cylinder_faces(
        mesh=mesh,
        vkey_lower=ref + "/bot/ring",
        vkey_upper=ref + "/top/ring",
        ref=ref + "/outer",
        norm_sign=+1.0,
    )

    if inner_radius is not None:
        mesh = cylinder.weave_cylinder_faces(
            mesh=mesh,
            vkey_lower=ref + "/bot/inner_ring",
            vkey_upper=ref + "/top/inner_ring",
            ref=ref + "/inner",
            norm_sign=-1.0,
        )

    return mesh
