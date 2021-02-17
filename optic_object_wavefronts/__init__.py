from .version import __version__
from . import plot
from . import Mesh
from . import geometry
from . import shapes


def _mesh_to_obj(mesh):
    """
    The mesh has human readable strings to reference vertices and normals.
    The object replaces those with numeric indices.
    """
    v_dict = {}
    for vi, vkey in enumerate(mesh["vertices"]):
        v_dict[vkey] = vi
    vn_dict = {}
    for vni, vnkey in enumerate(mesh["vertex_normals"]):
        vn_dict[vnkey] = vni

    obj = {
        "v": [],
        "vn": [],
        "f": [],
    }

    for vkey in mesh["vertices"]:
        obj["v"].append(mesh["vertices"][vkey])
    for vnkey in mesh["vertex_normals"]:
        obj["vn"].append(mesh["vertex_normals"][vnkey])

    for fkey in mesh["faces"]:
        vs = []
        for dim in range(3):
            vs.append(v_dict[mesh["faces"][fkey]["vertices"][dim]])
        vns = []
        for dim in range(3):
            vns.append(vn_dict[mesh["faces"][fkey]["vertex_normals"][dim]])
        obj["f"].append({"v": vs, "vn": vns})
    return obj


def _obj_to_wavefront(obj):
    # COUNTING STARTS AT ONE
    s = []
    s.append("# vertices")
    for v in obj["v"]:
        s.append("v {:f} {:f} {:f}".format(v[0], v[1], v[2]))
    s.append("# vertex-normals")
    for vn in obj["vn"]:
        s.append("vn {:f} {:f} {:f}".format(vn[0], vn[1], vn[2]))
    s.append("# faces")
    for f in obj["f"]:
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


def write_mesh(path, mesh, header=True):
    obj = _mesh_to_obj(mesh=mesh)
    wavefront = _obj_to_wavefront(obj=obj)
    with open(path, "wt") as fout:
        if header:
            fout.write("# {:s} v{:s}\n".format(__name__, __version__))
        fout.write(wavefront)
