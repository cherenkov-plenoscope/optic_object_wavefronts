
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


def init_from_mesh(mesh):
    """
    The mesh has hashable keys to address vertices and normals.
    The object-wavefront replaces those with numeric indices.
    """
    v_dict = {}
    for vi, vkey in enumerate(mesh["vertices"]):
        v_dict[vkey] = vi
    vn_dict = {}
    for vni, vnkey in enumerate(mesh["vertex_normals"]):
        vn_dict[vnkey] = vni

    object_wavefront = init()

    for vkey in mesh["vertices"]:
        object_wavefront["v"].append(mesh["vertices"][vkey])
    for vnkey in mesh["vertex_normals"]:
        object_wavefront["vn"].append(mesh["vertex_normals"][vnkey])

    for mkey in mesh["materials"]:
        object_wavefront["materials"][mkey] = []

        for fkey in mesh["faces"]:
            if _key_contains_any_of_patterns(key=fkey[0], patterns=mesh["materials"][mkey]):
                vs = []
                for dim in range(3):
                    vs.append(v_dict[mesh["faces"][fkey]["vertices"][dim]])
                vns = []
                for dim in range(3):
                    vns.append(vn_dict[mesh["faces"][fkey]["vertex_normals"][dim]])
                object_wavefront["materials"][mkey].append(
                    {"v": vs, "vn": vns}
                )

    return object_wavefront


def to_string(object_wavefront):
    # COUNTING STARTS AT ONE
    s = []
    s.append("# vertices")
    for v in object_wavefront["v"]:
        s.append("v {:f} {:f} {:f}".format(v[0], v[1], v[2]))
    s.append("# vertex-normals")
    for vn in object_wavefront["vn"]:
        s.append("vn {:f} {:f} {:f}".format(vn[0], vn[1], vn[2]))
    s.append("# faces")

    for mtl in object_wavefront["materials"]:
        s.append("usemtl {:s}".format(mtl))
        for f in object_wavefront["materials"][mtl]:
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
