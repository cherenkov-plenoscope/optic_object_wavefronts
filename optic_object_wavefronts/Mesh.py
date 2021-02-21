import copy
import collections


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
