from .. import Object
from . import disc
from . import template_cylinder
import numpy as np


def init(
    outer_radius=1.0, length=1.0, fn=6, rot=0.0, ref="cylinder",
):
    """
    Returns a cylinder-object.

    3D volume
    3 Materials: top / outer_side / bottom

    Parameters
    ----------
    outer_radius : float
            Outer radius of the regular polygon defining the disc.
    length : float
            Length of cylinder.
    fn : int
            Number of vertices in outer regular polygon.
    rot : float
            Rotation in z of regular polygon.
    ref : str
            Key for the material.
    """
    top = disc.init(
        outer_radius=outer_radius, ref=ref + "/top", fn=fn, rot=rot,
    )
    bot = disc.init(
        outer_radius=outer_radius,
        ref=ref + "/bot",
        fn=fn,
        rot=(2 * np.pi) / (2 * fn) + rot,
    )

    obj = Object.init()

    for vkey in top["vertices"]:
        tmp_v = np.array(top["vertices"][vkey])
        tmp_v[2] = float(length)
        obj["vertices"][vkey] = tmp_v
    for fkey in top["faces"]:
        obj["faces"][fkey] = top["faces"][fkey]
    for vnkey in top["vertex_normals"]:
        obj["vertex_normals"][vnkey] = [0, 0, 1]

    for vkey in bot["vertices"]:
        obj["vertices"][vkey] = bot["vertices"][vkey]
    for fkey in bot["faces"]:
        obj["faces"][fkey] = bot["faces"][fkey]
    for vnkey in bot["vertex_normals"]:
        obj["vertex_normals"][vnkey] = [0, 0, -1]

    obj = template_cylinder.weave_cylinder_faces(
        obj=obj,
        vkey_lower=ref + "/bot/outer_bound",
        vkey_upper=ref + "/top/outer_bound",
        ref=ref + "/outer",
    )

    obj["materials"][ref + "_top"] = ["top"]
    obj["materials"][ref + "_bottom"] = ["bot"]
    obj["materials"][ref + "_outer_side"] = ["outer"]

    return obj
