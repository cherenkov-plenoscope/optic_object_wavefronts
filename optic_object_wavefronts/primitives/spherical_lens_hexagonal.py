import numpy as np
from .. import Object
from . import cylinder
from . import spherical_cap_hexagonal


def estimate_height_of_cap(curvature_radius, outer_radius):
    return curvature_radius - np.sqrt(curvature_radius**2 - outer_radius**2)


def make_obj(
    outer_radius,
    curvature_radius,
    n,
    ref,
):
    assert curvature_radius > 0.0
    assert outer_radius > 0.0

    top = spherical_cap_hexagonal.make_obj(
        outer_radius=outer_radius,
        curvature_radius=-1.0 * curvature_radius,
        ref=ref + "/top",
        n=n,
    )
    bot = spherical_cap_hexagonal.make_obj(
        outer_radius=outer_radius,
        curvature_radius=1.0 * curvature_radius,
        ref=ref + "/bot",
        n=n,
    )

    cap_height = estimate_height_of_cap(curvature_radius, outer_radius)

    obj = Object.init()

    for vkey in top["vertices"]:
        tmp_v = np.array(top["vertices"][vkey])
        tmp_v[2] = tmp_v[2] + float(cap_height)
        obj["vertices"][vkey] = tmp_v
    for fkey in top["faces"]:
        obj["faces"][fkey] = top["faces"][fkey]
    for vnkey in top["vertex_normals"]:
        obj["vertex_normals"][vnkey] = +1.0 * top["vertex_normals"][vnkey]

    for vkey in bot["vertices"]:
        tmp_v = np.array(bot["vertices"][vkey])
        tmp_v[2] = tmp_v[2] - float(cap_height)
        obj["vertices"][vkey] = tmp_v
    for fkey in bot["faces"]:
        obj["faces"][fkey] = bot["faces"][fkey]
    for vnkey in bot["vertex_normals"]:
        obj["vertex_normals"][vnkey] = -1.0 * bot["vertex_normals"][vnkey]

    hexagonal_grid_spacing = outer_radius / n

    obj = spherical_cap_hexagonal.weave_hexagon_edges(
        obj=obj,
        outer_radius=outer_radius,
        margin_width_on_edge=0.1 * hexagonal_grid_spacing,
        ref=ref + "/side",
    )

    obj["materials"][ref+"_top"] = [ref + "/top"]
    obj["materials"][ref+"_bottom"] = [ref + "/bot"]
    obj["materials"][ref+"_side"] = [ref + "/side"]

    return obj
