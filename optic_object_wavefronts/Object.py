import copy
import collections
import numpy as np
from . import io
from . import version


def init():
    """
    Returns an Object which describes meshes of triangular faces.
    An Object can have multiple materials.
    This is the basic building.
    Finally it can be exported to an object-wavefront (.obj).
    """
    return {
        "vertices": collections.OrderedDict(),
        "vertex_normals": collections.OrderedDict(),
        "materials": collections.OrderedDict(),
    }


def translate(obj, v):
    """
    Returns a translated copy of the Object.

    Parameters
    ----------
    obj : dict
            The Object.
    v : numpy.array
            Three dimensional vector for translation.
    """
    v = np.array(v)
    out = copy.deepcopy(obj)
    for vkey in out["vertices"]:
        out["vertices"][vkey] += v
    return out


def merge(a, b):
    """
    Returns a new Object merged out of the objects a, and b.

    Parameters
    ----------
    a : dict
            The Object a.
    b : dict
            The Object b.
    """
    out = copy.deepcopy(a)
    for vkey in b["vertices"]:
        assert vkey not in out["vertices"]
        out["vertices"][vkey] = copy.deepcopy(b["vertices"][vkey])
    for vnkey in b["vertex_normals"]:
        assert vnkey not in out["vertex_normals"]
        out["vertex_normals"][vnkey] = copy.deepcopy(
            b["vertex_normals"][vnkey]
        )
    for mkey in b["materials"]:
        assert mkey not in out["materials"]
        out["materials"][mkey] = copy.deepcopy(b["materials"][mkey])
    return out


def remove_unused_vertices_and_vertex_normals(obj):
    """
    Returns a new Object with all unused vertices and vertex-normals removed.

    Parameters
    ----------
    obj : dict
            The Object.
    """
    out = init()
    out["materials"] = copy.deepcopy(obj["materials"])

    valid_vkeys = set()
    for mkey in out["materials"]:
        for fkey in out["materials"][mkey]:
            for vkey in out["materials"][mkey][fkey]["vertices"]:
                valid_vkeys.add(vkey)

    for vkey in obj["vertices"]:
        if vkey in valid_vkeys:
            out["vertices"][vkey] = obj["vertices"][vkey]

    valid_vnkeys = set()
    for mkey in out["materials"]:
        for fkey in out["materials"][mkey]:
            for vnkey in out["materials"][mkey][fkey]["vertex_normals"]:
                valid_vnkeys.add(vnkey)

    for vnkey in obj["vertex_normals"]:
        if vnkey in valid_vnkeys:
            out["vertex_normals"][vnkey] = obj["vertex_normals"][vnkey]

    return out


def write_to_wavefront(obj, path, header=True):
    """
    Writes the Object to a wavefront-file at path.

    Parameters
    ----------
    obj : dict
            The Object.
    path : str
            The output path.
    header : bool
            Add a header with version-number.
    """
    wavefront = io.obj.init_from_Object(obj)
    wavefront_str = io.obj.to_string(wavefront)
    with open(path, "wt") as fout:
        if header:
            fout.write("# {:s} v{:s}\n".format(__name__, version.__version__))
        fout.write(wavefront_str)
