from .. import mesh
from . import Disc
from . import TemplateCylinder
import numpy as np
import collections
import os


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
            Outer radius of the regular polygon defining the Disc.
    length : float
            Length of Cylinder.
    fn : int
            Number of vertices in outer regular polygon.
    rot : float
            Rotation in z of regular polygon.
    ref : str
            Key for the material.
    """
    top = Disc.init(
        outer_radius=outer_radius,
        ref=os.path.join(ref, "top"),
        fn=fn,
        rot=rot,
    )
    bot = Disc.init(
        outer_radius=outer_radius,
        ref=os.path.join(ref, "bot"),
        fn=fn,
        rot=(2 * np.pi) / (2 * fn) + rot,
    )

    cylinder = mesh.init()

    for vkey in top["vertices"]:
        tmp_v = np.array(top["vertices"][vkey])
        tmp_v[2] = float(length)
        cylinder["vertices"][vkey] = tmp_v
    for vnkey in top["vertex_normals"]:
        cylinder["vertex_normals"][vnkey] = np.array([0, 0, 1])

    mtl_top = os.path.join(ref, "top")
    cylinder["materials"][mtl_top] = collections.OrderedDict()
    for fkey in top["materials"][mtl_top]:
        cylinder["materials"][mtl_top][fkey] = top["materials"][mtl_top][fkey]

    for vkey in bot["vertices"]:
        cylinder["vertices"][vkey] = bot["vertices"][vkey]
    for vnkey in bot["vertex_normals"]:
        cylinder["vertex_normals"][vnkey] = np.array([0, 0, -1])

    mtl_bot = os.path.join(ref, "bot")
    cylinder["materials"][mtl_bot] = collections.OrderedDict()
    for fkey in bot["materials"][mtl_bot]:
        cylinder["materials"][mtl_bot][fkey] = bot["materials"][mtl_bot][fkey]

    cylinder = TemplateCylinder.weave_cylinder_faces(
        mesh=cylinder,
        vkey_lower=os.path.join(ref, "bot", "outer_bound"),
        vkey_upper=os.path.join(ref, "top", "outer_bound"),
        ref=os.path.join(ref, "outer"),
    )

    return cylinder