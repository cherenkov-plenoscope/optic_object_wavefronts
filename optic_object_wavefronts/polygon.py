"""
Polygons here are an ordered collection of vertices which are addressed
by keys in an ordered.dict.
"""
import numpy as np
import shapely
import collections
from shapely import geometry as shapely_geometry


def to_keys_and_numpy_array(polygon):
    """
    Parameters
    ----------
    polygon : dict
            The vertices of a polygon addressed by keys in a dict.

    Returns
    -------
    (keys, vertices) : tuple(list, numpy.array)
            A list of keys, and the plain coordinates of the vertices.
    """
    vertices = []
    keys = []
    for key in polygon:
        keys.append(key)
        vertices.append(polygon[key])
    vertices = np.array(vertices)
    return keys, vertices


def limits(polygon):
    """
    Returns the limits in x, y, and z of a polygon.

    Parameters
    ----------
    polygon : dict
            The vertices of a polygon addressed by keys in a dict.
    """
    _, p = to_keys_and_numpy_array(polygon=polygon)
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


def keep_vertices_in_mask(vertices, mask):
    """
    Returns a new dict containing only the vertices which are masked.
    """
    out = collections.OrderedDict()
    for i, vkey in enumerate(vertices):
        if mask[i]:
            out[vkey] = vertices[vkey]
    return out


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
    return keep_vertices_in_mask(
        vertices=vertices,
        mask=mask_vertices_inside(vertices, polygon),
    )


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
    mask_inside = mask_vertices_inside(vertices, polygon)
    return keep_vertices_in_mask(
        vertices=vertices,
        mask=np.logical_not(mask_inside),
    )


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

    shapely_poly = to_shapely_polygon(polygon)

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


def find_min_max_distant_to_point(polygon, point):
    """
    Parameters
    ----------
    polygon : dict
            The vertices of a polygon addressed by keys in a dict.
    point : array
            The x (point[0]) and y (point[1]) coordinates of the point.

    Returns
    -------
    (keys, distances) : tuple
        Keys itself is a tuple of the closest and furthest key of a vertex in
        the polygon.
        Distances is also a tuple of the closest and furthest distances.
    """
    max_distance = 0.0
    max_vkey = ""
    min_distance = float("inf")
    min_vkey = ""
    for vkey in polygon:
        vertex_x = polygon[vkey][0]
        vertex_y = polygon[vkey][1]
        delta_x = vertex_x - point[0]
        delta_y = vertex_y - point[1]
        distance = np.hypot(delta_x, delta_y)
        if distance >= max_distance:
            max_distance = distance
            max_vkey = str(vkey)
        if distance < min_distance:
            min_distance = distance
            min_vkey = str(vkey)

    return (min_vkey, max_vkey), (min_distance, max_distance)


def rotate_z(polygon, theta):
    out = collections.OrderedDict()
    for key in polygon:
        x, y, z = polygon[key]
        nx = np.cos(theta) * x - np.sin(theta) * y
        ny = np.sin(theta) * x + np.cos(theta) * y
        out[key] = np.array([nx, ny, z])
    return out


def translate(polygon, translation):
    translation = np.array(translation)
    out = collections.OrderedDict()
    for key in polygon:
        pos = np.array(polygon[key])
        out[key] = pos + translation
    return out
