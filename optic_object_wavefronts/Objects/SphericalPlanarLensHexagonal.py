from . import SphericalCapHexagonal
from . import Disc
from .. import Object
import numpy as np


def init(
    outer_radius,
    curvature_radius,
    width,
    fn=10,
    ref="SphericalPlaneHexagonalBody",
):
    front_obj = SphericalCapHexagonal.init(
        outer_radius=outer_radius,
        curvature_radius=curvature_radius,
        fn=fn,
        ref=ref + "/front",
    )

    back_obj = Disc.init(
        outer_radius=outer_radius, fn=6, ref=ref + "/back", rot=0.0,
    )

    center_of_curvature = np.array([0.0, 0.0, curvature_radius])

    back_obj = Object.translate(back_obj, [0.0, 0.0, -width])
    for vnkey in back_obj["vertex_normals"]:
        back_obj["vertex_normals"][vnkey] = np.array([0.0, 0.0, -1.0])

    obj = Object.merge(front_obj, back_obj)

    hexagonal_grid_spacing = outer_radius / fn

    obj = SphericalCapHexagonal.weave_hexagon_edges(
        obj=obj,
        outer_radius=outer_radius,
        margin_width_on_edge=0.1 * hexagonal_grid_spacing,
        ref=ref + "/side",
    )

    # remove /side faces inside of curvature-sphere
    side_fkeys = []
    for fkey in obj["faces"]:
        if str.find(fkey[0], ref + "/side") >= 0:
            side_fkeys.append(fkey)

    for fkey in side_fkeys:
        va_key = obj["faces"][fkey]["vertices"][0]
        vb_key = obj["faces"][fkey]["vertices"][1]
        vc_key = obj["faces"][fkey]["vertices"][2]

        va = obj["vertices"][va_key]
        vb = obj["vertices"][vb_key]
        vc = obj["vertices"][vc_key]

        mid_ab = 0.5 * (va + vb)
        mid_bc = 0.5 * (vb + vc)
        mid_ca = 0.5 * (vc + va)

        r_mid_ab = np.linalg.norm(mid_ab - center_of_curvature)
        r_mid_bc = np.linalg.norm(mid_bc - center_of_curvature)
        r_mid_ca = np.linalg.norm(mid_ca - center_of_curvature)

        mid_ab_inside = r_mid_ab <= curvature_radius
        mid_bc_inside = r_mid_bc <= curvature_radius
        mid_ca_inside = r_mid_ca <= curvature_radius

        if np.sum([mid_ab_inside, mid_bc_inside, mid_ca_inside]) > 1:
            obj["faces"].pop(fkey)

    obj["materials"] = {}
    obj["materials"][ref + "_front"] = [ref + "/front"]
    obj["materials"][ref + "_back"] = [ref + "/back"]
    obj["materials"][ref + "_side"] = [ref + "/side"]

    return obj
