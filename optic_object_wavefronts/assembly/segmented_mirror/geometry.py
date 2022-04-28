import numpy as np
from ... import polygon
from ... import geometry


def init_facet_supports_on_principal_aperture_plane(
    aperture_outer_polygon,
    aperture_inner_polygon,
    grid_spacing,
    grid_style="hexagonal",
    center_of_grid=[0.0, 0.0],
):
    _, min_max_distances = polygon.find_min_max_distant_to_point(
        polygon=aperture_outer_polygon, point=center_of_grid
    )
    outer_radius = min_max_distances[1]

    fN = 2 * int(np.ceil(outer_radius / grid_spacing))

    if grid_style == "hexagonal":
        _grid = geometry.grid.hexagonal.make_vertices_xy(
            outer_radius=1.0, ref="hex", fn=fN
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

    mask_valid = np.logical_and(mask_inside_outer, mask_outside_inner)

    grid = []
    for i in range(len(_grid)):
        if mask_valid[i]:
            grid.append(_grid[i])
    grid = np.array(grid)
    return grid
