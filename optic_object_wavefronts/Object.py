import copy
import collections
from . import Wavefront
from . import version

def init():
    return {
        "vertices": collections.OrderedDict(),
        "faces": collections.OrderedDict(),
        "vertex_normals": collections.OrderedDict(),
        "materials": collections.OrderedDict(),
    }


def translate(obj, v):
    out = copy.deepcopy(obj)
    for vkey in out["vertices"]:
        out["vertices"][vkey] += v
    return out


def merge(a, b):
    out = copy.deepcopy(a)
    for vkey in b["vertices"]:
        assert vkey not in out["vertices"]
        out["vertices"][vkey] = copy.deepcopy(b["vertices"][vkey])
    for vnkey in b["vertex_normals"]:
        assert vnkey not in out["vertex_normals"]
        out["vertex_normals"][vnkey] = copy.deepcopy(
            b["vertex_normals"][vnkey]
        )
    for fkey in b["faces"]:
        assert fkey not in out["faces"]
        out["faces"][fkey] = copy.deepcopy(b["faces"][fkey])

    for mkey in b["materials"]:
        assert mkey not in out["materials"]
        out["materials"][mkey] = copy.deepcopy(b["materials"][mkey])
    return out


def remove_unused_vertices_and_vertex_normals(obj):
    out = init()
    out["faces"] = copy.deepcopy(obj["faces"])
    out["materials"] = copy.deepcopy(obj["materials"])

    valid_vkeys = set()
    for fkey in obj["faces"]:
        for vkey in obj["faces"][fkey]["vertices"]:
            valid_vkeys.add(vkey)

    for vkey in obj["vertices"]:
        if vkey in valid_vkeys:
            out["vertices"][vkey] = obj["vertices"][vkey]

    valid_vnkeys = set()
    for fkey in obj["faces"]:
        for vnkey in obj["faces"][fkey]["vertex_normals"]:
            valid_vnkeys.add(vnkey)

    for vnkey in obj["vertex_normals"]:
        if vnkey in valid_vnkeys:
            out["vertex_normals"][vnkey] = obj["vertex_normals"][vnkey]

    return out


def write_to_wavefront(obj, path, header=True):
    wavefront = Wavefront.init_from_Object(obj)
    wavefront_str = Wavefront.to_string(wavefront)
    with open(path, "wt") as fout:
        if header:
            fout.write("# {:s} v{:s}\n".format(__name__, version.__version__))
        fout.write(wavefront_str)
