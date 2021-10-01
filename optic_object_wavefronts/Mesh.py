import copy
import collections
from . import ObjectWavefront
from . import version

def init():
    return {
        "vertices": collections.OrderedDict(),
        "faces": collections.OrderedDict(),
        "vertex_normals": collections.OrderedDict(),
        "materials": collections.OrderedDict(),
    }


def translate(mesh, v):
    out = copy.deepcopy(mesh)
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


def remove_unused_vertices_and_vertex_normals(mesh):
    out = init()
    out["faces"] = copy.deepcopy(mesh["faces"])
    out["materials"] = copy.deepcopy(mesh["materials"])

    valid_vkeys = set()
    for fkey in mesh["faces"]:
        for vkey in mesh["faces"][fkey]["vertices"]:
            valid_vkeys.add(vkey)

    for vkey in mesh["vertices"]:
        if vkey in valid_vkeys:
            out["vertices"][vkey] = mesh["vertices"][vkey]

    valid_vnkeys = set()
    for fkey in mesh["faces"]:
        for vnkey in mesh["faces"][fkey]["vertex_normals"]:
            valid_vnkeys.add(vnkey)

    for vnkey in mesh["vertex_normals"]:
        if vnkey in valid_vnkeys:
            out["vertex_normals"][vnkey] = mesh["vertex_normals"][vnkey]

    return out


def write_to_object_wavefront(mesh, path, header=True):
    obj = ObjectWavefront.init_from_mesh(mesh)
    obj_str = ObjectWavefront.to_string(obj)
    with open(path, "wt") as fout:
        if header:
            fout.write("# {:s} v{:s}\n".format(__name__, version.__version__))
        fout.write(obj_str)
