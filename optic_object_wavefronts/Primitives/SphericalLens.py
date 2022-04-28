import numpy as np
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
        ref=ref + "/top",
        fn_polygon=fn_polygon,
        fn_hex_grid=fn_hex_grid,
        rot=rot,
    )
    bot = SphericalCapRegular.init(
        outer_radius=outer_radius,
        inner_radius=inner_radius,
        curvature_radius=-1.0 * curvature_radius_bot,
        ref=ref + "/bot",
        fn_polygon=fn_polygon,
        fn_hex_grid=fn_hex_grid,
        rot=(2 * np.pi) / (2 * fn_polygon) + rot,
    )

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

    obj = TemplateCylinder.weave_cylinder_faces(
        obj=obj,
        vkey_lower=ref + "/bot/outer_bound",
        vkey_upper=ref + "/top/outer_bound",
        ref=ref + "/outer",
        norm_sign=+1.0,
    )

    if inner_radius is not None:
        obj = TemplateCylinder.weave_cylinder_faces(
            obj=obj,
            vkey_lower=ref + "/bot/inner_bound",
            vkey_upper=ref + "/top/inner_bound",
            ref=ref + "/inner",
            norm_sign=-1.0,
        )

    obj["materials"][ref + "_top"] = [ref + "/top"]
    obj["materials"][ref + "_bottom"] = [ref + "/bot"]
    obj["materials"][ref + "_outer_side"] = [ref + "/outer"]
    if inner_radius is not None:
        obj["materials"][ref + "_inner_side"] = [ref + "/inner"]

    return obj
