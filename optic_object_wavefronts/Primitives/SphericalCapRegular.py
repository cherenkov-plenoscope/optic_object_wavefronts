from .. import Geometry
from . import SphericalCap


def init(
    outer_radius,
    curvature_radius,
    inner_radius=None,
    fn_polygon=17,
    fn_hex_grid=10,
    ref="SphericalCap",
    rot=0.0,
):
    outer_polygon = Geometry.RegularPolygon.make_vertices_xy(
        outer_radius=outer_radius,
        fn=fn_polygon,
        ref=ref + "/outer_bound",
        rot=rot,
    )

    if inner_radius is not None:
        inner_polygon = Geometry.RegularPolygon.make_vertices_xy(
            outer_radius=inner_radius,
            fn=fn_polygon,
            ref=ref + "/inner_bound",
            rot=rot,
        )
    else:
        inner_polygon = None

    return SphericalCap.init(
        outer_polygon=outer_polygon,
        inner_polygon=inner_polygon,
        fn_hex_grid=fn_hex_grid,
        curvature_radius=curvature_radius,
        ref=ref,
    )