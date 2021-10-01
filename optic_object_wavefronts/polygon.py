"""
Polygons here are an ordered collection of vertices which are addressed
by keys in an ordered.dict.
"""
import numpy as np
import shapely
import collections
from shapely import geometry as shapely_geometry


def to_numpy_array(polygon):
    """
    Returns a numpy.array() of the vertices in the polygon.
    All addressing keys are lost.

    Parameters
    ----------
    polygon : dict
            The vertices of a polygon addressed by keys in a dict.
    """
    arr = []
    for k in polygon:
        arr.append(polygon[k])
    return np.array(arr)


def limits(polygon):
    """
    Returns the limits in x, y, and z of a polygon.

    Parameters
    ----------
    polygon : dict
            The vertices of a polygon addressed by keys in a dict.
    """
    p = to_numpy_array(polygon)
    return (
        [np.min(p[:, 0]), np.max(p[:, 0])],
        [np.min(p[:, 1]), np.max(p[:, 1])],
        [np.min(p[:, 2]), np.max(p[:, 2])],
    )


def to_shapely_polygon(polygon):
    """
    Returns a shapely.geometry.Polygon() of the vertices in the polygon.
    All addressing keys are lost.

    Parameters
    ----------
    polygon : dict
            The vertices of a polygon addressed by keys in a dict.
    """

    poly = []
    for pkey in polygon:
        poly.append((polygon[pkey][0], polygon[pkey][1]))
    _line = shapely.geometry.LineString(poly)
    return shapely.geometry.Polygon(_line)


def mask_vertices_inside(vertices, polygon):
    """
    Returns a list of bools, one bool for each vertex, to mark if it is
    inside the polygon.

    Parameters
    ----------
    vertices : dict
            The vertices addressed by keys in a dict.
    polygon : dict
            The vertices of a polygon addressed by keys in a dict.
    """
    _polygon = to_shapely_polygon(polygon)
    mask = []
    for vkey in vertices:
        _point = shapely.geometry.Point(vertices[vkey][0], vertices[vkey][1])
        mask.append(_polygon.contains(_point))
    return mask


def get_vertices_inside(vertices, polygon):
    """
    Returns a new dict containing only the vertices inside the polygon.

    Parameters
    ----------
    vertices : dict
            The vertices addressed by keys in a dict.
    polygon : dict
            The vertices of a polygon addressed by keys in a dict.

    Compare
    -------
    mask_vertices_inside()
    """
    out = collections.OrderedDict()
    mask = mask_vertices_inside(vertices, polygon)
    for i, vkey in enumerate(vertices):
        if mask[i]:
            out[vkey] = vertices[vkey]
    return out


def get_vertices_outside(vertices, polygon):
    """
    Returns a new dict containing only the vertices outside the polygon.

    Parameters
    ----------
    vertices : dict
            The vertices addressed by keys in a dict.
    polygon : dict
            The vertices of a polygon addressed by keys in a dict.

    Compare
    -------
    mask_vertices_inside()
    get_vertices_inside()
    """
    out = collections.OrderedDict()
    mask = mask_vertices_inside(vertices, polygon)
    for i, vkey in enumerate(vertices):
        if not mask[i]:
            out[vkey] = vertices[vkey]
    return out


def mask_face_inside(vertices, faces, polygon):
    """
    Returns a list of bools, one pool for each face, to mask if it is
    inside the polygon.

    Parameters
    ----------
    vertices : dict
            The vertices of the faces addressed by keys in a dict.
    faces : dict
            The faces which reference their vertices by keys.
            Faces a addressed by keys themselves in a dict.
    polygon : dict
            The vertices of a polygon addressed by keys in a dict.
    """

    shapely_poly = _to_shapely_polygon(polygon)

    mask = []
    for fkey in faces:
        vkey_a = faces[fkey]["vertices"][0]
        vkey_b = faces[fkey]["vertices"][1]
        vkey_c = faces[fkey]["vertices"][2]

        va = vertices[vkey_a]
        vb = vertices[vkey_b]
        vc = vertices[vkey_c]

        mid_ab = 0.5 * (va + vb)
        mid_bc = 0.5 * (vb + vc)
        mid_ca = 0.5 * (vc + va)

        _point_ab = shapely.geometry.Point(mid_ab[0], mid_ab[1])
        _point_bc = shapely.geometry.Point(mid_bc[0], mid_bc[1])
        _point_ca = shapely.geometry.Point(mid_ca[0], mid_ca[1])

        hit_ab = shapely_poly.contains(_point_ab)
        hit_bc = shapely_poly.contains(_point_bc)
        hit_ca = shapely_poly.contains(_point_ca)

        if np.sum([hit_ab, hit_bc, hit_ca]) > 1:
            mask.append(True)
        else:
            mask.append(False)

    return mask
