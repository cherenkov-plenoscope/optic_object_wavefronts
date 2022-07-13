"""
Create segmented mirrors from parameters.
"""
import numpy as np
import collections
from ... import Polygon
from ... import Geometry

CONFIG = {
    "aperture_outer_polygon": Geometry.RegularPolygon.make_vertices_xy(
        outer_radius=80,
        ref="aperture_outer_polygon",
        fn=6,
        rot=0.0,
    ),
}


def init_facet_supports_on_principal_aperture_plane(
    aperture_outer_polygon=Geometry.RegularPolygon.make_vertices_xy(
        outer_radius=1.0
    ),
    aperture_inner_polygon=Geometry.RegularPolygon.make_vertices_xy(
        outer_radius=0.5
    ),
    grid_spacing=0.1,
    grid_style="hexagonal",
    center_of_grid=[0.0, 0.0],
    ref="grid",
):
    _, min_max_distances = Polygon.find_min_max_distant_to_point(
        polygon=aperture_outer_polygon, point=center_of_grid
    )
    outer_radius = min_max_distances[1]

    fN = 2 * int(np.ceil(outer_radius / grid_spacing))

    if grid_style == "hexagonal":
        _grid = Geometry.Grid.Hexagonal.init_from_spacing(
            spacing=grid_spacing, ref=ref, fN=fN
        )
    elif grid_style == "rectangular":
        _grid = Geometry.Grid.Rectangular.init_from_spacing(
            spacing=grid_spacing, ref=ref, fN=fN
        )
    else:
        assert False, "Grid style {:s} is unknown.".format(grid_style)

    mask_inside_outer = Polygon.mask_vertices_inside(
        vertices=_grid, polygon=aperture_outer_polygon
    )
    mask_inside_inner = Polygon.mask_vertices_inside(
        vertices=_grid, polygon=aperture_inner_polygon
    )
    mask_outside_inner = np.logical_not(mask_inside_inner)

    mask = np.logical_and(mask_inside_outer, mask_outside_inner)

    return Polygon.keep_vertices_in_mask(vertices=_grid, mask=mask)


def elevate_facet_supports(
    facet_supports,
    curvature_height_function=Geometry.Parabola.surface_height,
    curvature_config={"focal_length": 10.0},
):
    out = collections.OrderedDict(facet_supports)
    for fkey in out:
        out[fkey][2] = curvature_height_function(
            x=out[fkey][0], y=out[fkey][1], **curvature_config,
        )
    return out


def init_facet_rotation(
    facet_support,
    point_to_reflect_light_to,
    direction_of_light_travel=[0.0, 0.0, -1.0],
):
    facet_support = np.array(facet_support)

    direction_of_light_travel = np.array(direction_of_light_travel)
    _direction_of_light_travel_norm = np.linalg.norm(direction_of_light_travel)
    assert _direction_of_light_travel_norm > 0.0
    direction_of_light_travel /= _direction_of_light_travel_norm
    direction_of_light_coming_from = -1.0 * direction_of_light_travel

    point_to_reflect_light_to = np.array(point_to_reflect_light_to)

    direction_facet_to_target = -facet_support + point_to_reflect_light_to
    direction_facet_to_target_norm = np.linalg.norm(direction_facet_to_target)
    assert direction_facet_to_target_norm > 0.0
    direction_facet_to_target /= direction_facet_to_target_norm

    rotation_axis = np.cross(direction_facet_to_target, direction_of_light_coming_from)

    return 1

