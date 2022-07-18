import numpy as np
import os
import collections
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

    side_mtl = os.path.join(ref, "side")
    obj["materials"][side_mtl] = collections.OrderedDict()

    for ni in range(n):
        n_a = int(ni)
        n_b = int(n_a + 1)
        if n_b == n:
            n_b = 0
        n_c = int(ni)
        va_key = os.path.join(vkey_upper, "{:06d}".format(n_a))
        va = np.array(obj["vertices"][va_key])
        vb_key = os.path.join(vkey_upper, "{:06d}".format(n_b))
        vb = np.array(obj["vertices"][vb_key])
        vc_key = os.path.join(vkey_lower, "{:06d}".format(n_c))
        vc = np.array(obj["vertices"][vc_key])
        va[2] = 0.0
        vb[2] = 0.0
        vc[2] = 0.0

        rst_vna_key = os.path.join(ref, "side", "top", "{:06d}".format(n_a))
        if rst_vna_key not in obj["vertex_normals"]:
            obj["vertex_normals"][rst_vna_key] = (
                norm_sign * va / np.linalg.norm(va)
            )

        rst_vnb_key = os.path.join(ref, "side", "top", "{:06d}".format(n_b))
        if rst_vnb_key not in obj["vertex_normals"]:
            obj["vertex_normals"][rst_vnb_key] = (
                norm_sign * vb / np.linalg.norm(vb)
            )

        rsb_vnc_key = os.path.join(ref, "side", "bot", "{:06d}".format(n_c))
        if rsb_vnc_key not in obj["vertex_normals"]:
            obj["vertex_normals"][rsb_vnc_key] = (
                norm_sign * vc / np.linalg.norm(vc)
            )

        obj["materials"][side_mtl]["ttb_{:06d}".format(ni)] = {
            "vertices": [
                va_key,
                vb_key,
                vc_key,
            ],
            "vertex_normals": [
                rst_vna_key,
                rst_vnb_key,
                rsb_vnc_key,
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
        va_key = os.path.join(vkey_lower, "{:06d}".format(n_a))
        va = np.array(obj["vertices"][va_key])
        vb_key = os.path.join(vkey_lower, "{:06d}".format(n_b))
        vb = np.array(obj["vertices"][vb_key])
        vc_key = os.path.join(vkey_upper, "{:06d}".format(n_c))
        vc = np.array(obj["vertices"][vc_key])
        va[2] = 0.0
        vb[2] = 0.0
        vc[2] = 0.0

        rsb_vna_key = os.path.join(ref, "side", "bot", "{:06d}".format(n_a))
        if rsb_vna_key not in obj["vertex_normals"]:
            obj["vertex_normals"][rsb_vna_key] = (
                norm_sign * va / np.linalg.norm(va)
            )

        rsb_vnb_key = os.path.join(ref, "side", "bot", "{:06d}".format(n_b))
        if rsb_vnb_key not in obj["vertex_normals"]:
            obj["vertex_normals"][rsb_vnb_key] = (
                norm_sign * vb / np.linalg.norm(vb)
            )

        rst_vnc_key = os.path.join(ref, "side", "top", "{:06d}".format(n_c))
        if rst_vnc_key not in obj["vertex_normals"]:
            obj["vertex_normals"][rst_vnc_key] = (
                norm_sign * vc / np.linalg.norm(vc)
            )

        obj["materials"][side_mtl]["bbt_{:06d}".format(ni)] = {
            "vertices": [
                va_key,
                vb_key,
                vc_key,
            ],
            "vertex_normals": [
                rsb_vna_key,
                rsb_vnb_key,
                rst_vnc_key,
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
        vkey_lower=os.path.join(ref, "bot", "outer_bound"),
        vkey_upper=os.path.join(ref, "top", "outer_bound"),
        ref=os.path.join(ref, "outer"),
        norm_sign=+1.0,
    )

    if weave_inner_polygon:
        obj = weave_cylinder_faces(
            obj=obj,
            vkey_lower=os.path.join(ref, "bot", "inner_bound"),
            vkey_upper=os.path.join(ref, "top", "inner_bound"),
            ref=os.path.join(ref, "inner"),
            norm_sign=-1.0,
        )

    return obj
