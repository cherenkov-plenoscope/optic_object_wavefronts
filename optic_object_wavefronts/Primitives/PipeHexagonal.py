from .. import Object
import numpy as np


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
                vkey = ref + "/w{:s}{:s}{:d}".format(h, j, i)
                obj["vertices"][vkey] = [rcos, rsin, hhh[h]]

    # vertex normals
    # --------------
    for i in range(6):
        obj["vertex_normals"][ref + "/vni{:d}".format(i)] = vn[i]
        obj["vertex_normals"][ref + "/vno{:d}".format(i)] = -1.0 * vn[i]
    obj["vertex_normals"][ref + "/vnbot"] = [0, 0, -1]
    obj["vertex_normals"][ref + "/vntop"] = [0, 0, 1]

    vnbot = ref + "/vnbot"
    vntop = ref + "/vntop"
    # faces
    # -----
    for i in range(6):
        vnikey = ref + "/vni{:d}".format(i)
        vnokey = ref + "/vno{:d}".format(i)
        li = i
        li1 = np.mod(i + 1, 6)
        # inner walls
        # -----------
        obj["faces"][(ref + "/inner", (i, 0))] = {
            "vertices": [
                ref + "/wli{:d}".format(li),
                ref + "/wli{:d}".format(li1),
                ref + "/whi{:d}".format(li),
            ],
            "vertex_normals": [vnikey, vnikey, vnikey],
        }
        obj["faces"][(ref + "/inner", (i, 1))] = {
            "vertices": [
                ref + "/whi{:d}".format(li1),
                ref + "/whi{:d}".format(li),
                ref + "/wli{:d}".format(li1),
            ],
            "vertex_normals": [vnikey, vnikey, vnikey],
        }
        # outer walls
        # -----------
        obj["faces"][(ref + "/outer", (i, 0))] = {
            "vertices": [
                ref + "/wlo{:d}".format(li),
                ref + "/wlo{:d}".format(li1),
                ref + "/who{:d}".format(li),
            ],
            "vertex_normals": [vnokey, vnokey, vnokey],
        }
        obj["faces"][(ref + "/outer", (i, 1))] = {
            "vertices": [
                ref + "/who{:d}".format(li1),
                ref + "/who{:d}".format(li),
                ref + "/wlo{:d}".format(li1),
            ],
            "vertex_normals": [vnokey, vnokey, vnokey],
        }
        # bottom faces
        # ------------
        obj["faces"][(ref + "/bottom", (i, 0))] = {
            "vertices": [
                ref + "/wli{:d}".format(li),
                ref + "/wli{:d}".format(li1),
                ref + "/wlo{:d}".format(li),
            ],
            "vertex_normals": [vnbot, vnbot, vnbot],
        }
        obj["faces"][(ref + "/bottom", (i, 1))] = {
            "vertices": [
                ref + "/wli{:d}".format(li1),
                ref + "/wlo{:d}".format(li1),
                ref + "/wlo{:d}".format(li),
            ],
            "vertex_normals": [vnbot, vnbot, vnbot],
        }
        # top faces
        # ---------
        obj["faces"][(ref + "/top", (i, 0))] = {
            "vertices": [
                ref + "/whi{:d}".format(li),
                ref + "/whi{:d}".format(li1),
                ref + "/who{:d}".format(li),
            ],
            "vertex_normals": [vntop, vntop, vntop],
        }
        obj["faces"][(ref + "/top", (i, 1))] = {
            "vertices": [
                ref + "/whi{:d}".format(li1),
                ref + "/who{:d}".format(li1),
                ref + "/who{:d}".format(li),
            ],
            "vertex_normals": [vntop, vntop, vntop],
        }

    obj["materials"][ref + "_inner"] = [ref + "/inner"]
    obj["materials"][ref + "_top"] = [ref + "/top"]
    obj["materials"][ref + "_bottom"] = [ref + "/bottom"]
    obj["materials"][ref + "_outer"] = [ref + "/outer"]
    return obj
