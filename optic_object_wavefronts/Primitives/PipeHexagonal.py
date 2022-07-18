from .. import Object
import numpy as np
import os
import collections


def init(
    outer_radius, inner_radius, height, ref="PipeHexagonal",
):
    """
    A hexagonal pipe with inner, and outer walls.

    Parameters
    ----------
    outer_radius : float
        Outer radius of the outer hexagon.
    inner_radius : float
        Outer radius of the inner hexagon.
    height : float
        Height of the pipe.
    """
    join = os.path.join

    assert outer_radius > 0
    assert inner_radius > 0
    assert outer_radius > inner_radius
    assert height > 0

    ro = outer_radius
    ri = inner_radius
    rrr = {"i": ri, "o": ro}
    hhh = {"l": 0.0, "h": height}
    obj = Object.init()

    # vertices
    # --------
    vn = []
    for h in hhh:
        for j in rrr:
            for i in range(6):
                cos = np.cos(2.0 / 6.0 * np.pi * i)
                sin = np.sin(2.0 / 6.0 * np.pi * i)
                rcos = rrr[j] * cos
                rsin = rrr[j] * sin
                vn.append(np.array([cos, sin, 0.0]))
                vkey = join(ref, "w{:s}{:s}{:d}".format(h, j, i))
                obj["vertices"][vkey] = [rcos, rsin, hhh[h]]

    # vertex normals
    # --------------
    for i in range(6):
        obj["vertex_normals"][join(ref, "vni{:d}".format(i))] = vn[i]
        obj["vertex_normals"][join(ref, "vno{:d}".format(i))] = -1.0 * vn[i]
    obj["vertex_normals"][join(ref, "vnbot")] = [0, 0, -1]
    obj["vertex_normals"][join(ref, "vntop")] = [0, 0, 1]

    vnbot = join(ref, "vnbot")
    vntop = join(ref, "vntop")

    mtl_inner_key = join(ref, "inner")
    obj["materials"][mtl_inner_key] = collections.OrderedDict()

    mtl_outer_key = join(ref, "outer")
    obj["materials"][mtl_outer_key] = collections.OrderedDict()

    mtl_bottom_key = join(ref, "bottom")
    obj["materials"][mtl_bottom_key] = collections.OrderedDict()

    mtl_top_key = join(ref, "top")
    obj["materials"][mtl_top_key] = collections.OrderedDict()

    # faces
    # -----
    for i in range(6):
        vnikey = join(ref, "vni{:d}".format(i))
        vnokey = join(ref, "vno{:d}".format(i))
        li = i
        li1 = np.mod(i + 1, 6)

        # inner walls
        # -----------
        obj["materials"][mtl_inner_key]["{:d}_{:d}".format(i, 0)] = {
            "vertices": [
                join(ref, "wli{:d}".format(li)),
                join(ref, "wli{:d}".format(li1)),
                join(ref, "whi{:d}".format(li)),
            ],
            "vertex_normals": [vnikey, vnikey, vnikey],
        }
        obj["materials"][mtl_inner_key]["{:d}_{:d}".format(i, 1)] = {
            "vertices": [
                join(ref, "whi{:d}".format(li1)),
                join(ref, "whi{:d}".format(li)),
                join(ref, "wli{:d}".format(li1)),
            ],
            "vertex_normals": [vnikey, vnikey, vnikey],
        }

        # outer walls
        # -----------
        obj["materials"][mtl_outer_key]["{:d}_{:d}".format(i, 0)] = {
            "vertices": [
                join(ref, "wlo{:d}".format(li)),
                join(ref, "wlo{:d}".format(li1)),
                join(ref, "who{:d}".format(li)),
            ],
            "vertex_normals": [vnokey, vnokey, vnokey],
        }
        obj["materials"][mtl_outer_key]["{:d}_{:d}".format(i, 1)] = {
            "vertices": [
                join(ref, "who{:d}".format(li1)),
                join(ref, "who{:d}".format(li)),
                join(ref, "wlo{:d}".format(li1)),
            ],
            "vertex_normals": [vnokey, vnokey, vnokey],
        }

        # bottom faces
        # ------------
        obj["materials"][mtl_bottom_key]["{:d}_{:d}".format(i, 0)] = {
            "vertices": [
                join(ref, "wli{:d}".format(li)),
                join(ref, "wli{:d}".format(li1)),
                join(ref, "wlo{:d}".format(li)),
            ],
            "vertex_normals": [vnbot, vnbot, vnbot],
        }
        obj["materials"][mtl_bottom_key]["{:d}_{:d}".format(i, 1)] = {
            "vertices": [
                join(ref, "wli{:d}".format(li1)),
                join(ref, "wlo{:d}".format(li1)),
                join(ref, "wlo{:d}".format(li)),
            ],
            "vertex_normals": [vnbot, vnbot, vnbot],
        }

        # top faces
        # ---------
        obj["materials"][mtl_top_key]["{:d}_{:d}".format(i, 0)] = {
            "vertices": [
                join(ref, "whi{:d}".format(li)),
                join(ref, "whi{:d}".format(li1)),
                join(ref, "who{:d}".format(li)),
            ],
            "vertex_normals": [vntop, vntop, vntop],
        }
        obj["materials"][mtl_top_key]["{:d}_{:d}".format(i, 1)] = {
            "vertices": [
                join(ref, "whi{:d}".format(li1)),
                join(ref, "who{:d}".format(li1)),
                join(ref, "who{:d}".format(li)),
            ],
            "vertex_normals": [vntop, vntop, vntop],
        }

    return obj
