"""
Create segmented mirrors from parameters.
"""
import numpy as np
import collections
import copy
from ... import Geometry
from ... import polygon
from ... import Primitives
from ... import materials


CONFIG_EXAMPLE = {
    "focal_length": 4.889,
    "DaviesCotton_over_parabolic_mixing_factor": 0.5,
    "max_outer_aperture_radius": 2.1,
    "min_inner_aperture_radius": 0.2,
    "outer_aperture_shape_hex": 0,
    "facet_inner_hex_radius": 0.30,
    "gap_between_facets": 0.01,
}


def add_segmented_mirror_to_frame_in_scenery(
    frame,
    scenery,
    config=CONFIG_EXAMPLE,
    outer_medium="vacuum",
    inner_medium="vacuum",
    facet_surface_mirror="perfect_mirror",
    facet_surface_body="perfect_absorber",
    facet_fn=7,
    facet_body_width=0.0,
    ref="a",
):
    """
    Parameters
    ----------
    frame : dict
        A frame in the scenery.
    scenery : dict
        The scenery.
    config : dict
        The geometry of the working-surface in Sebastian's format used since
        his Master-thesis.
    outer_medium : str
        Key of the outer medium sourroundung the mirror.
    inner_medium : str
        Key of the inner medium inside the facets.
    facet_surface_mirror : str
        Key of the facets working-surface.
    facet_surface_body : str
        Key of the facets body surface.
    facet_body_width : float
        If 0, the facets do not have bodys but only the working surface.
        Smallest width of facet's body from back to working-surface.
    facet_fn : int
        Density of vertices and faces in facet.
    ref : str
        A name to distinguish this mirror from others.
    """

    # facet
    # -----
    facet_outer_radius = config["facet_inner_hex_radius"] * (
        2.0 / np.sqrt(3.0)
    )
    facet_curvature_radius = 2.0 * config["focal_length"]
    facet_object_key = ref + "facet"

    scenery["materials"]["boundary_layers"][ref + "f"] = {
        "inner": {"medium": inner_medium, "surface": facet_surface_body},
        "outer": {"medium": outer_medium, "surface": facet_surface_mirror},
    }

    if facet_body_width > 0.0:
        facet = Primitives.SphericalPlanarLensHexagonal.init(
            outer_radius=facet_outer_radius,
            curvature_radius=facet_curvature_radius,
            width=facet_body_width,
            fn=facet_fn,
            ref="facet",
        )
        facet_mtl_to_boundary_layers_map = {
            "facet/front": ref + "f",
            "facet/back": ref + "b",
            "facet/side": ref + "b",
        }
        scenery["materials"]["boundary_layers"][ref + "b"] = {
            "inner": {"medium": inner_medium, "surface": facet_surface_body},
            "outer": {"medium": outer_medium, "surface": facet_surface_body},
        }
    else:
        facet = Primitives.SphericalCapHexagonal.init(
            outer_radius=facet_outer_radius,
            curvature_radius=facet_curvature_radius,
            fn=facet_fn,
            ref="facet",
        )
        facet_mtl_to_boundary_layers_map = {
            "facet": ref + "f",
        }

    # add objects
    # -----------
    assert facet_object_key not in scenery["objects"]
    scenery["objects"][facet_object_key] = facet

    # add media
    # ---------
    for medium_key in [outer_medium, inner_medium]:
        if medium_key not in scenery["materials"]["media"]:
            scenery["materials"]["media"][medium_key] = materials.medium(
                key=medium_key
            )

    # add surfaces
    # ------------
    for surface_key in [facet_surface_mirror, facet_surface_body]:
        if surface_key not in scenery["materials"]["surfaces"]:
            scenery["materials"]["surfaces"][surface_key] = materials.surface(
                key=surface_key
            )

    # facet-supports
    # --------------
    approx_num_facets_on_outer_radius = (
        config["max_outer_aperture_radius"] / config["facet_inner_hex_radius"]
    )

    fn_circle = int(np.ceil(2.0 * np.pi * approx_num_facets_on_outer_radius))
    grid_spacing = (
        2.0 * config["facet_inner_hex_radius"] + config["gap_between_facets"]
    )

    # outer bound xy
    # --------------
    outer_radius_facet_supports = (
        config["max_outer_aperture_radius"] - config["facet_inner_hex_radius"]
    )
    inner_radius_facet_supports = (
        config["min_inner_aperture_radius"] + config["facet_inner_hex_radius"]
    )

    if config["outer_aperture_shape_hex"] == 1:
        aperture_outer_polygon = Geometry.regular_polygon.make_vertices_xy(
            outer_radius=outer_radius_facet_supports, fn=6, rot=np.pi / 6,
        )
    else:
        aperture_outer_polygon = Geometry.regular_polygon.make_vertices_xy(
            outer_radius=outer_radius_facet_supports, fn=fn_circle, rot=0.0,
        )

    facet_centers = init_facet_centers_xy(
        aperture_outer_polygon=aperture_outer_polygon,
        aperture_inner_polygon=Geometry.regular_polygon.make_vertices_xy(
            outer_radius=inner_radius_facet_supports, fn=fn_circle,
        ),
        grid_spacing=grid_spacing,
        grid_style="hexagonal",
        grid_rotation=np.pi / 2,
        center_of_grid=[0.0, 0.0],
        ref="facet_centers",
    )

    facet_centers = set_facet_centers_z(
        facet_centers=facet_centers,
        focal_length=config["focal_length"],
        DaviesCotton_over_parabolic_mixing_factor=config[
            "DaviesCotton_over_parabolic_mixing_factor"
        ],
        max_delta=1e-6 * config["focal_length"],
        max_iterations=1000,
    )

    # orientation
    # -----------
    focal_point = [0, 0, config["focal_length"]]
    facet_id = 0
    for fkey in facet_centers:
        child = {
            "id": int(facet_id),
            "pos": facet_centers[fkey],
            "rot": init_facet_rotation(
                facet_center=facet_centers[fkey], focal_point=focal_point,
            ),
            "obj": facet_object_key,
            "mtl": facet_mtl_to_boundary_layers_map,
        }
        frame["children"].append(child)
        facet_id += 1

    return scenery


def init_facet_centers_xy(
    aperture_outer_polygon=Geometry.regular_polygon.make_vertices_xy(
        outer_radius=1.0
    ),
    aperture_inner_polygon=Geometry.regular_polygon.make_vertices_xy(
        outer_radius=0.5
    ),
    grid_spacing=0.1,
    grid_style="hexagonal",
    grid_rotation=np.pi / 2,
    center_of_grid=[0.0, 0.0],
    ref="grid",
):
    _, min_max_distances = polygon.find_min_max_distant_to_point(
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

    _grid = polygon.rotate_z(_grid, grid_rotation)
    mask_inside_outer = polygon.mask_vertices_inside(
        vertices=_grid, polygon=aperture_outer_polygon
    )
    mask_inside_inner = polygon.mask_vertices_inside(
        vertices=_grid, polygon=aperture_inner_polygon
    )
    mask_outside_inner = np.logical_not(mask_inside_inner)
    mask = np.logical_and(mask_inside_outer, mask_outside_inner)
    return polygon.keep_vertices_in_mask(vertices=_grid, mask=mask)


def set_facet_centers_z(
    facet_centers,
    focal_length,
    DaviesCotton_over_parabolic_mixing_factor,
    max_delta,
    max_iterations=1000,
):
    assert focal_length > 0.0
    assert 0 <= DaviesCotton_over_parabolic_mixing_factor <= 1.0
    for fkey in facet_centers:
        davies_cotton_z = Geometry.sphere.surface_height(
            x=facet_centers[fkey][0],
            y=facet_centers[fkey][1],
            curvature_radius=focal_length,
        )
        prabola_z = Geometry.Parabola.surface_height(
            x=facet_centers[fkey][0],
            y=facet_centers[fkey][1],
            focal_length=focal_length,
        )
        a = DaviesCotton_over_parabolic_mixing_factor
        facet_z = a * davies_cotton_z + (1 - a) * prabola_z
        facet_centers[fkey][2] = facet_z

    # fine tune z
    # -----------
    focal_point = [0.0, 0.0, focal_length]
    i = 0
    while True:
        delta = focal_length - vertices_mean_distance_to_vertex(
            vertices=facet_centers, vertex=focal_point,
        )
        if delta < max_delta:
            break
        i += 1
        assert i < max_iterations
        shift = [0.0, 0.0, -delta / 2]
        facet_centers = vertices_add(vertices=facet_centers, vertex=shift)
    return facet_centers


def vertices_mean_distance_to_vertex(vertices, vertex):
    vertex = np.array(vertex)
    distances = []
    for fkey in vertices:
        d = np.linalg.norm(vertex - vertices[fkey])
        distances.append(d)
    return np.mean(distances)


def vertices_add(vertices, vertex):
    vertex = np.array(vertex)
    for fkey in vertices:
        vertices[fkey] += vertex
    return vertices


def init_facet_rotation(
    facet_center, focal_point, direction_incoming_light=[0.0, 0.0, -1.0],
):
    facet_center = np.array(facet_center)

    focal_point = np.array(focal_point)

    direction_incoming_light = np.array(direction_incoming_light)
    _direction_of_light_travel_norm = np.linalg.norm(direction_incoming_light)
    assert _direction_of_light_travel_norm > 0.0
    direction_incoming_light /= _direction_of_light_travel_norm
    direction_of_light_coming_from = -1.0 * direction_incoming_light

    direction_facet_to_target = -facet_center + focal_point
    direction_facet_to_target_norm = np.linalg.norm(direction_facet_to_target)
    assert direction_facet_to_target_norm > 0.0
    direction_facet_to_target /= direction_facet_to_target_norm

    rotation_angle = -0.5 * np.arccos(
        np.dot(direction_facet_to_target, direction_of_light_coming_from)
    )

    if np.abs(rotation_angle) > 0.0:
        rotation_axis = np.cross(
            direction_facet_to_target, direction_of_light_coming_from
        )
        return {
            "repr": "axis_angle",
            "axis": rotation_axis.tolist(),
            "angle_deg": float(np.rad2deg(rotation_angle)),
        }
    else:
        return {"repr": "tait_bryan", "xyz_deg": [0, 0, 0]}
