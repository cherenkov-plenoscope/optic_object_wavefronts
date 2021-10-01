
def _key_contains_any_of_patterns(key, patterns):
    for pattern in patterns:
        if str.find(key, pattern) >= 0:
            return True
    return False


def init():
    return {
        "v": [],
        "vn": [],
        "materials": {},
    }


def init_from_Object(obj):
    """
    The obj has hashable keys to address vertices and normals.
    The object-wavefront replaces those with numeric indices.
    """
    v_dict = {}
    for vi, vkey in enumerate(obj["vertices"]):
        v_dict[vkey] = vi
    vn_dict = {}
    for vni, vnkey in enumerate(obj["vertex_normals"]):
        vn_dict[vnkey] = vni

    wavefront = init()

    for vkey in obj["vertices"]:
        wavefront["v"].append(obj["vertices"][vkey])
    for vnkey in obj["vertex_normals"]:
        wavefront["vn"].append(obj["vertex_normals"][vnkey])

    for mkey in obj["materials"]:
        wavefront["materials"][mkey] = []

        for fkey in obj["faces"]:
            if _key_contains_any_of_patterns(key=fkey[0], patterns=obj["materials"][mkey]):
                vs = []
                for dim in range(3):
                    vs.append(v_dict[obj["faces"][fkey]["vertices"][dim]])
                vns = []
                for dim in range(3):
                    vns.append(vn_dict[obj["faces"][fkey]["vertex_normals"][dim]])
                wavefront["materials"][mkey].append(
                    {"v": vs, "vn": vns}
                )

    return wavefront


def to_string(wavefront):
    # COUNTING STARTS AT ONE
    s = []
    s.append("# vertices")
    for v in wavefront["v"]:
        s.append("v {:f} {:f} {:f}".format(v[0], v[1], v[2]))
    s.append("# vertex-normals")
    for vn in wavefront["vn"]:
        s.append("vn {:f} {:f} {:f}".format(vn[0], vn[1], vn[2]))
    s.append("# faces")

    for mtl in wavefront["materials"]:
        s.append("usemtl {:s}".format(mtl))
        for f in wavefront["materials"][mtl]:
            s.append(
                "f {:d}//{:d} {:d}//{:d} {:d}//{:d}".format(
                    1 + f["v"][0],
                    1 + f["vn"][0],
                    1 + f["v"][1],
                    1 + f["vn"][1],
                    1 + f["v"][2],
                    1 + f["vn"][2],
                )
            )
    return "\n".join(s) + "\n"
