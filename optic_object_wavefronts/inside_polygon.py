import shapely
from shapely import geometry as shapely_geometry


def mask_vertices(vertices, polygon):
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


def get_vertices(vertices, polygon):
    out = {}
    mask = mask_vertices(vertices, polygon)
    for i, vkey in enumerate(vertices):
        if mask[i]:
            out[vkey] = vertices[vkey]
    return out
