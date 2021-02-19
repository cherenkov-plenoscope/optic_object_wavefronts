import copy


def init():
    return {"vertices": {}, "faces": {}, "vertex_normals": {}}


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
        if vnkey in out["vertex_normals"]:
            print(vnkey)
        assert vnkey not in out["vertex_normals"]
        out["vertex_normals"][vnkey] = copy.deepcopy(
            b["vertex_normals"][vnkey]
        )
    for fkey in b["faces"]:
        assert fkey not in out["faces"]
        out["faces"][fkey] = copy.deepcopy(b["faces"][fkey])
    return out
