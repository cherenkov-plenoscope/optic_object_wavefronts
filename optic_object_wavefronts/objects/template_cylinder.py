import numpy as np
from .. import Object


def _find_keys(dic, key):
    out = []
    for k in dic:
        if key in k:
            out.append(k)
    return out


def weave_cylinder_faces(obj, ref, vkey_lower, vkey_upper, norm_sign=1.0):
    assert np.abs(norm_sign) == 1.0

    num_v_lower = len(_find_keys(dic=obj["vertices"], key=vkey_lower))
    num_v_upper = len(_find_keys(dic=obj["vertices"], key=vkey_upper))
    assert num_v_lower == num_v_upper
    n = num_v_upper

    for ni in range(n):
        n_a = int(ni)
        n_b = int(n_a + 1)
        if n_b == n:
            n_b = 0
        n_c = int(ni)
        va = np.array(obj["vertices"][(vkey_upper, n_a)])
        vb = np.array(obj["vertices"][(vkey_upper, n_b)])
        vc = np.array(obj["vertices"][(vkey_lower, n_c)])
        va[2] = 0.0
        vb[2] = 0.0
        vc[2] = 0.0
        if (ref + "/side/top", n_a) not in obj["vertex_normals"]:
            obj["vertex_normals"][(ref + "/side/top", n_a)] = (
                norm_sign * va / np.linalg.norm(va)
            )

        if (ref + "/side/top", n_b) not in obj["vertex_normals"]:
            obj["vertex_normals"][(ref + "/side/top", n_b)] = (
                norm_sign * vb / np.linalg.norm(vb)
            )

        if (ref + "/side/bot", n_c) not in obj["vertex_normals"]:
            obj["vertex_normals"][(ref + "/side/bot", n_c)] = (
                norm_sign * vc / np.linalg.norm(vc)
            )

        side_fkey = (ref + "/side_ttb", ni)
        obj["faces"][side_fkey] = {
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
        va = np.array(obj["vertices"][(vkey_lower, n_a)])
        vb = np.array(obj["vertices"][(vkey_lower, n_b)])
        vc = np.array(obj["vertices"][(vkey_upper, n_c)])
        va[2] = 0.0
        vb[2] = 0.0
        vc[2] = 0.0
        if (ref + "/side/bot", n_a) not in obj["vertex_normals"]:
            obj["vertex_normals"][(ref + "/side/bot", n_a)] = (
                norm_sign * va / np.linalg.norm(va)
            )

        if (ref + "/side/bot", n_b) not in obj["vertex_normals"]:
            obj["vertex_normals"][(ref + "/side/bot", n_b)] = (
                norm_sign * vb / np.linalg.norm(vb)
            )

        if (ref + "/side/top", n_c) not in obj["vertex_normals"]:
            obj["vertex_normals"][(ref + "/side/top", n_c)] = (
                norm_sign * vc / np.linalg.norm(vc)
            )

        side_fkey = (ref + "/side_bbt", ni)
        obj["faces"][side_fkey] = {
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

    return obj


def init(
    top_surface_object,
    bot_surface_object,
    offset,
    fn_polygon,
    fn_hex_grid,
    ref,
    weave_inner_polygon,
):
    top = top_surface_object
    bot = bot_surface_object

    obj = Object.init()

    for vkey in top["vertices"]:
        tmp_v = np.array(top["vertices"][vkey])
        # tmp_v[2] = tmp_v[2] + 0.5 * float(offset)
        obj["vertices"][vkey] = tmp_v
    for fkey in top["faces"]:
        obj["faces"][fkey] = top["faces"][fkey]
    for vnkey in top["vertex_normals"]:
        obj["vertex_normals"][vnkey] = +1.0 * top["vertex_normals"][vnkey]

    for vkey in bot["vertices"]:
        tmp_v = np.array(bot["vertices"][vkey])
        tmp_v[2] = tmp_v[2] - float(offset)
        obj["vertices"][vkey] = tmp_v
    for fkey in bot["faces"]:
        obj["faces"][fkey] = bot["faces"][fkey]
    for vnkey in bot["vertex_normals"]:
        obj["vertex_normals"][vnkey] = -1.0 * bot["vertex_normals"][vnkey]

    obj = weave_cylinder_faces(
        obj=obj,
        vkey_lower=ref + "/bot/outer_bound",
        vkey_upper=ref + "/top/outer_bound",
        ref=ref + "/outer",
        norm_sign=+1.0,
    )

    if weave_inner_polygon:
        obj = weave_cylinder_faces(
            obj=obj,
            vkey_lower=ref + "/bot/inner_bound",
            vkey_upper=ref + "/top/inner_bound",
            ref=ref + "/inner",
            norm_sign=-1.0,
        )

    obj["materials"][ref + "_top"] = [ref + "/top"]
    obj["materials"][ref + "_bottom"] = [ref + "/bot"]
    obj["materials"][ref + "_outer_side"] = [ref + "/outer"]
    if weave_inner_polygon:
        obj["materials"][ref + "_inner_side"] = [ref + "/inner"]

    return obj
