import numpy as np
import collections
from ... import polygon
from ... import Geometry


def init_facet_supports_on_principal_aperture_plane(
    aperture_outer_polygon=Geometry.regular_polygon.make_vertices_xy(outer_radius=1.0),
    aperture_inner_polygon=Geometry.regular_polygon.make_vertices_xy(outer_radius=0.5),
    grid_spacing=0.1,
    grid_style="hexagonal",
    center_of_grid=[0.0, 0.0],
    ref="grid",
):
    _, min_max_distances = polygon.find_min_max_distant_to_point(
        polygon=aperture_outer_polygon, point=center_of_grid
    )
    outer_radius = min_max_distances[1]

    fN = 2 * int(np.ceil(outer_radius / grid_spacing))

    if grid_style == "hexagonal":
        _grid = Geometry.grid.hexagonal.init_from_spacing(
            spacing=grid_spacing, ref=ref, fN=fN
        )
    elif grid_style == "rectangular":
        _grid = Geometry.grid.rectangular.init_from_spacing(
            spacing=grid_spacing, ref=ref, fN=fN
        )
    else:
        assert False, "Grid style {:s} is unknown.".format(grid_style)

    mask_inside_outer = polygon.mask_vertices_inside(
        vertices=_grid, polygon=aperture_outer_polygon
    )
    mask_inside_inner = polygon.mask_vertices_inside(
        vertices=_grid, polygon=aperture_inner_polygon
    )
    mask_outside_inner = np.logical_not(mask_inside_inner)

    mask = np.logical_and(mask_inside_outer, mask_outside_inner)

    return polygon.keep_vertices_in_mask(vertices=_grid, mask=mask)


def elevate_facet_supports(
    facet_supports,
    curvature_height_function=Geometry.parabola.surface_height,
    curvature_config={"focal_length": 10.0},
):
    out = collections.OrderedDict(facet_supports)
    for fkey in out:
        out[fkey][2] = curvature_height_function(
            x=out[fkey][0],
            y=out[fkey][1],
            **curvature_config,
        )
    return out
