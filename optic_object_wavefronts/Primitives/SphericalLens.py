import numpy as np
import os
import collections
from .. import Object
from . import TemplateCylinder
from . import SphericalCapRegular


def init(
    outer_radius,
    curvature_radius_top,
    curvature_radius_bot,
    offset,
    fn_polygon,
    fn_hex_grid,
    rot,
    ref,
    inner_radius=None,
):
    top = SphericalCapRegular.init(
        outer_radius=outer_radius,
        inner_radius=inner_radius,
        curvature_radius=-1.0 * curvature_radius_top,
        ref=os.path.join(ref, "top"),
        fn_polygon=fn_polygon,
        fn_hex_grid=fn_hex_grid,
        rot=rot,
    )
    bot = SphericalCapRegular.init(
        outer_radius=outer_radius,
        inner_radius=inner_radius,
        curvature_radius=-1.0 * curvature_radius_bot,
        ref=os.path.join(ref, "bot"),
        fn_polygon=fn_polygon,
        fn_hex_grid=fn_hex_grid,
        rot=(2 * np.pi) / (2 * fn_polygon) + rot,
    )

    obj = Object.init()

    for vkey in top["vertices"]:
        tmp_v = np.array(top["vertices"][vkey])
        # tmp_v[2] = tmp_v[2] + 0.5 * float(offset)
        obj["vertices"][vkey] = tmp_v

    top_mtl_key = os.path.join(ref, "top")
    obj["materials"][top_mtl_key] = collections.OrderedDict()
    for fkey in top["materials"][top_mtl_key]:
        obj["materials"][top_mtl_key][fkey] = top["materials"][top_mtl_key][fkey]

    for vnkey in top["vertex_normals"]:
        obj["vertex_normals"][vnkey] = +1.0 * top["vertex_normals"][vnkey]

    for vkey in bot["vertices"]:
        tmp_v = np.array(bot["vertices"][vkey])
        tmp_v[2] = tmp_v[2] - float(offset)
        obj["vertices"][vkey] = tmp_v

    bot_mtl_key = os.path.join(ref, "bot")
    obj["materials"][bot_mtl_key] = collections.OrderedDict()
    for fkey in bot["materials"][bot_mtl_key]:
        obj["materials"][bot_mtl_key][fkey] = bot["materials"][bot_mtl_key][fkey]

    for vnkey in bot["vertex_normals"]:
        obj["vertex_normals"][vnkey] = -1.0 * bot["vertex_normals"][vnkey]

    obj = TemplateCylinder.weave_cylinder_faces(
        obj=obj,
        vkey_lower=os.path.join(ref, "bot", "outer_bound"),
        vkey_upper=os.path.join(ref, "top", "outer_bound"),
        ref=os.path.join(ref, "outer"),
        norm_sign=+1.0,
    )

    if inner_radius is not None:
        obj = TemplateCylinder.weave_cylinder_faces(
            obj=obj,
            vkey_lower=os.path.join(ref, "bot", "inner_bound"),
            vkey_upper=os.path.join(ref, "top", "inner_bound"),
            ref=os.path.join(ref + "inner"),
            norm_sign=-1.0,
        )

    return obj
