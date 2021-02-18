import numpy as np
import shapely
from shapely import geometry as shapely_geometry


def to_np_array(polygon_vertices):
    arr = []
    for k in polygon_vertices:
        arr.append(polygon_vertices[k])
    return np.array(arr)


def limits(polygon_vertices):
    a = to_np_array(polygon_vertices)

    return (
        [np.min(a[:, 0]), np.max(a[:, 0])],
        [np.min(a[:, 1]), np.max(a[:, 1])],
        [np.min(a[:, 2]), np.max(a[:, 2])],
    )


def _to_shapely_polygon(polygon):
    poly = []
    for pkey in polygon:
        poly.append((polygon[pkey][0], polygon[pkey][1]))
    _line = shapely.geometry.LineString(poly)
    return shapely.geometry.Polygon(_line)


def mask_vertices_inside(vertices, polygon):
    _polygon = _to_shapely_polygon(polygon)
    mask = []
    for vkey in vertices:
        _point = shapely.geometry.Point(vertices[vkey][0], vertices[vkey][1])
        mask.append(_polygon.contains(_point))
    return mask


def get_vertices_inside(vertices, polygon):
    out = {}
    mask = mask_vertices_inside(vertices, polygon)
    for i, vkey in enumerate(vertices):
        if mask[i]:
            out[vkey] = vertices[vkey]
    return out


def get_vertices_outside(vertices, polygon):
    out = {}
    mask = mask_vertices_inside(vertices, polygon)
    for i, vkey in enumerate(vertices):
        if not mask[i]:
            out[vkey] = vertices[vkey]
    return out


def mask_face_inside(vertices, faces, polygon):
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
