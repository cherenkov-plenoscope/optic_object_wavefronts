import numpy as np


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
            if _key_contains_any_of_patterns(
                key=fkey[0], patterns=obj["materials"][mkey]
            ):
                vs = []
                for dim in range(3):
                    vs.append(v_dict[obj["faces"][fkey]["vertices"][dim]])
                vns = []
                for dim in range(3):
                    vns.append(
                        vn_dict[obj["faces"][fkey]["vertex_normals"][dim]]
                    )
                wavefront["materials"][mkey].append({"v": vs, "vn": vns})

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


def init_from_vertices_and_faces_only(vertices, faces, mtl="material_name"):
    """
    Returns a wavefron-dictionary.
    Vertext-normals 'vn' are created based on the faces surface-normals.
    The wavefront has only one material 'mtl' named 'mtl'.

    Parameters
    ----------
    vertices : list/array of vertices
        The 3D-vertices of the mesh.
    faces : list/array of faces
        The faces (triangles) which reference 3 vertices each.
    mtl : str
        The name of the only material in the output wavefront.
    """
    all_vns = _make_normals_from_faces(vertices=vertices, faces=faces)
    unique_vns, unique_vn_map = _group_normals(all_vns)

    wavefront = init()
    wavefront["materials"][mtl] = []

    for v in vertices:
        wavefront["v"].append(v)

    for vn in unique_vns:
        wavefront["vn"].append(vn)

    for i in range(len(faces)):
        face = faces[i]
        ff = {}
        fv = [face[0], face[1], face[2]]

        ff["v"] = fv
        unique_vn_i = unique_vn_map[i]
        fvn = [unique_vn_i, unique_vn_i, unique_vn_i]

        ff["vn"] = fvn
        wavefront["materials"][mtl].append(ff)

    return wavefront


def _make_normal_from_face(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    a_to_b = b - a
    a_to_c = c - a
    n = np.cross(a_to_b, a_to_c)
    n = n / np.linalg.norm(n)
    return n


def _make_normals_from_faces(vertices, faces):
    normals = []
    for f in faces:
        a = vertices[f[0]]
        b = vertices[f[1]]
        c = vertices[f[2]]
        n = _make_normal_from_face(a=a, b=b, c=c)
        normals.append(n)
    return normals


def _group_normals(normals):
    """
    Identify equal normals so that those can be shared by faces.
    This reduces storage space in obj-files and accelerates raytracing.
    """
    nset = set()
    unique_normals = []
    unique_map = []
    unique_i = -1
    for i in range(len(normals)):
        normal = normals[i]
        ntuple = (normal[0], normal[1], normal[2])
        if ntuple not in nset:
            nset.add(ntuple)
            unique_i += 1
            unique_normals.append(normal)
        unique_map.append(unique_i)

    return unique_normals, unique_map
