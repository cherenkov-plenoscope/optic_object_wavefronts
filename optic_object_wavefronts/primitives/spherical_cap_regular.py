from .. import geometry
from . import spherical_cap

def init(
    outer_radius,
    curvature_radius,
    inner_radius=None,
    n_polygon=17,
    n_hex_grid=10,
    ref="SphericalCap",
    rot=0.0,
):
    outer_polygon = geometry.regular_polygon.make_vertices_xy(
        outer_radius=outer_radius,
        n=n_polygon,
        ref=ref + "/ring",
        rot=rot,
    )

    if inner_radius is not None:
        inner_polygon = geometry.regular_polygon.make_vertices_xy(
            outer_radius=inner_radius,
            n=n_polygon,
            ref=ref + "/inner_ring",
            rot=rot,
        )
    else:
        inner_polygon = None

    return spherical_cap.init(
        outer_polygon=outer_polygon,
        inner_polygon=inner_polygon,
        n_hex_grid=n_hex_grid,
        curvature_radius=curvature_radius,
        ref=ref
    )
