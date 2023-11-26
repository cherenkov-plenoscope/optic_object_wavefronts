import numpy as np
import os
import scipy
from scipy import spatial as scipy_spatial
from . import polygon
import collections


def make_faces_xy(vertices, ref):
    """
    Create triangular faces based on the vertices x, and y components.

    Parameters
    ----------
    vertices : dict
            The vertices to make triangular faces for.
    ref : str
            The key for the faces keys.

    Returns
    -------
    faces : dict
            The faces for the vertices, referencing the vertices by key.
    """
    vkeys, vertices = polygon.to_keys_and_numpy_array(polygon=vertices)
    vertices_xy = vertices[:, 0:2]

    del_tri = scipy.spatial.Delaunay(points=vertices_xy)
    del_faces = del_tri.simplices

    faces = {}
    for fidx, del_face in enumerate(del_faces):
        fkey = os.path.join(ref, "{:06d}".format(fidx))
        faces[fkey] = {
            "vertices": [
                vkeys[del_face[0]],
                vkeys[del_face[1]],
                vkeys[del_face[2]],
            ],
        }
    return faces


def fill_polygon_xy(poly, vertices):
    """
    Inserts additional vertives into the polygon 'poly' in order to make
    sure that the points along the polygon are closer to each other than to
    the outer vertices.
    This ensures that delauny triangles will a not cross the segments of the
    polygon.
    This is important e.g. for inner polygons which are not perfectly convex
    but have carvings.
    Only the xy-components are considered.

    Parameters
    ----------
    poly : OrderedDict (str, 3d array)
        A closed loop polygon
    vertices : dict (str, 3d array)
        Vertices of the mesh (excluding the vertices of the polygon)

    Returns
    -------
    poly : OrderedDict (str, 3d array)
        Same vertices as in the input poly but with additional vertices in
        between when needed.
    """
    vxy = np.zeros(shape=(len(vertices), 2), dtype=float)
    vnames = []
    for i, vkey in enumerate(vertices):
        vxy[i] = vertices[vkey][0:2]
        vnames.append(vkey)

    tree = scipy_spatial.cKDTree(data=vxy)

    outpoly = collections.OrderedDict()

    vkeys = list(poly.keys())
    for s in range(len(vkeys)):
        start_vkey, stop_key = cycle_segment_keys(vkeys, s)
        vstart = poly[start_vkey]
        vstop = poly[stop_key]

        segment = Line(start=vstart[0:2], stop=vstop[0:2])

        matches_start = set(
            tree.query_ball_point(x=vstart[0:2], r=segment.length)
        )
        matches_stop = set(
            tree.query_ball_point(x=vstop[0:2], r=segment.length)
        )
        matches = list(matches_start.union(matches_stop))

        inter_match = []
        inter_paras = []
        for vmatch in matches:
            para = segment.parameter_for_closest_distance_to_point(vxy[vmatch])
            if 0 <= para <= segment.length:
                inter_match.append(vmatch)
                inter_paras.append(para)
        inter_match = np.array(inter_match)
        inter_paras = np.array(inter_paras)

        # sort based on segment parameter
        sarg = np.argsort(inter_paras)
        inter_match = inter_match[sarg]
        inter_paras = inter_paras[sarg]

        outpoly[start_vkey] = poly[start_vkey]
        for i in range(len(inter_match)):
            inter_vkey = start_vkey + "/projection/{:s}".format(
                vnames[inter_match[i]]
            )
            interpoint_2d = segment.at(parameter=inter_paras[i])
            outpoly[inter_vkey] = np.array(
                [interpoint_2d[0], interpoint_2d[1], 0.0]
            )

    outpoly[stop_key] = poly[stop_key]
    return outpoly


class Line:
    def __init__(self, start, stop):
        self.support = start
        self.length = np.linalg.norm(stop - start)
        self.direction = (stop - start) / self.length

    def parameter_for_closest_distance_to_point(self, point):
        d = np.dot(self.direction, point)
        return d - np.dot(self.support, self.direction)

    def at(self, parameter):
        return self.support + parameter * self.direction

    def projection_of_point(self, point):
        parameter = self.parameter_for_closest_distance_to_point(point)
        if 0 <= parameter <= self.length:
            return self.at(parameter)
        else:
            None


def cycle_segment_keys(keys, i):
    start, stop = cycle_segment(num=len(keys), i=i)
    return keys[start], keys[stop]


def cycle_segment(num, i):
    assert num >= 0
    i = i % num
    j = i + 1
    j = j % num
    return i, j
