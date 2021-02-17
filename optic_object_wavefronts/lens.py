from . import Mesh
from . import regular_polygon
from . import delaunay
import numpy as np
import os
import scipy
from scipy import spatial as scipy_spatial
import shapely
from shapely import geometry as shapely_geometry


HEXA = np.array([1.0, 0.0, 0.0])
HEXB = np.array([0.5, np.sqrt(3.0) / 2.0, 0.0])


def make_hex_grid(outer_radius=1.0, ref="hex", n=10):
    spacing = float(outer_radius/n)
    N = int(n)
    vertices = {}
    for dA in np.arange(-N, N + 1, 1):
        for dB in np.arange(-N, N + 1, 1):
            bound_upper = -dA + N
            bound_lower = -dA - N
            if dB <= bound_upper and dB >= bound_lower:
                vertices[(ref, (dA, dB))] = (dA * HEXA + dB * HEXB) * spacing
    return vertices


def make_hex_mesh_in_regular_polygon(outer_radius, n_poly, n_hex, ref="HexGridInPoly"):
    g = make_hex_grid(outer_radius=outer_radius*1.5, ref=os.path.join(ref, "hex"), n=n_hex)
    r = regular_polygon.make_vertices_xy(outer_radius=outer_radius, ref=os.path.join(ref, "ring"), n=n_poly, rot=0.0)

    mesh = Mesh.init()

    mesh["vertices"] = vertices_inside_polygon(vertices=g, polygon=r)
    for vkey in r:
        mesh["vertices"][vkey] = r[vkey]

    vnkey = (ref, 0)
    mesh["vertex_normals"][vnkey] = np.array([0.0, 0.0, 1.0])

    faces = delaunay.make_faces_xy(vertices=mesh["vertices"], ref=ref)

    for fkey in faces:
        mesh["faces"][fkey] = {
            "vertices": faces[fkey]["vertices"],
            "vertex_normals": [vnkey, vnkey, vnkey],
        }
    return mesh



def mask_vertices_inside_polygon(vertices, polygon):
    poly = []
    for pkey in polygon:
        poly.append((polygon[pkey][0], polygon[pkey][1]))

    _line = shapely.geometry.LineString(poly)
    _polygon = shapely.geometry.Polygon(_line)
    mask = []
    for vkey in vertices:
        _point = shapely.geometry.Point(vertices[vkey][0], vertices[vkey][1])
        mask.append(_polygon.contains(_point))
    return mask


def vertices_inside_polygon(vertices, polygon):
    out = {}
    mask = mask_vertices_inside_polygon(vertices, polygon)
    for i, vkey in enumerate(vertices):
        if mask[i]:
            out[vkey] = vertices[vkey]
    return out
