"""
Create segmented mirrors from parameters.
"""
import numpy as np
import collections
import copy
import os
from .. import geometry
from .. import polygon
from .. import primitives
from .. import materials
from . import light_field_sensor_camera_module
from . import segmented_mirror


CONFIG_EXAMPLE = {
    "expected_imaging_system_focal_length": 16.0,
    "expected_imaging_system_max_aperture_radius": 5.0,
    "max_FoV_diameter": np.deg2rad(4.5),
    "pixel_FoV_hex_flat2flat": np.deg2rad(0.2),
    "housing_overhead": 0,
    "num_paxel_on_pixel_diagonal": 5,
    "curved": 1,
}


def make_geometry(
    imaging_system_focal_length,
    imaging_system_diameter,
    field_of_view_polygon,
    field_of_view_camera,
    camera_points_towards_center_of_imaging_system,
):
    assert imaging_system_focal_length > 0.0
    assert imaging_system_diameter > 0.0
    assert len(field_of_view_polygon) >= 3

    assert field_of_view_camera > 0.0

    c = {}
    c["imaging_system"] = {}
    c["imaging_system"]["focal_length"] = float(imaging_system_focal_length)
    c["imaging_system"]["diameter"] = float(imaging_system_diameter)
    c["imaging_system"]["radius"] = 0.5 * c["imaging_system"]["diameter"]
    c["imaging_system"]["fstop"] = (
        c["imaging_system"]["focal_length"] / c["imaging_system"]["diameter"]
    )
    c["imaging_system"]["center"] = np.array(
        [0.0, 0.0, -c["imaging_system"]["focal_length"]]
    )

    c["field_of_view"] = {}
    _, c["field_of_view"]["polygon"] = polygon.to_keys_and_numpy_array(
        polygon=field_of_view_polygon
    )

    (
        c["field_of_view"]["cxlim"],
        c["field_of_view"]["cylim"],
        _,
    ) = polygon.limits(polygon=field_of_view_polygon)

    cxout = np.max(np.abs(c["field_of_view"]["cxlim"]))
    cyout = np.max(np.abs(c["field_of_view"]["cylim"]))
    safe_radial_angle = 1.2 * np.hypot(cxout, cyout)

    c["camera"] = {}
    c["camera"]["field_of_view"] = float(field_of_view_camera)
    c["camera"]["spacing"] = (
        c["camera"]["field_of_view"] * c["imaging_system"]["focal_length"]
    )

    grid_fn = int(np.ceil(safe_radial_angle / c["camera"]["field_of_view"]))
    camera_directions = geometry.grid.hexagonal.init_from_spacing(
        spacing=c["camera"]["field_of_view"],
        ref="camera_directions",
        fN=grid_fn,
    )
    camera_directions = polygon.get_vertices_inside(
        vertices=camera_directions,
        polygon=field_of_view_polygon,
    )
    c["camera"]["centers"] = {}
    for ci, ckey in enumerate(camera_directions):
        nckey = "camera{:06d}".format(ci)
        c["camera"]["centers"][ckey] = (
            c["imaging_system"]["focal_length"] * camera_directions[ckey]
        )
    c["camera"]["rotations"] = {}

    if camera_points_towards_center_of_imaging_system:
        for ckey in c["camera"]["centers"]:
            sphere_z = geometry.sphere.surface_height(
                x=c["camera"]["centers"][ckey][0],
                y=c["camera"]["centers"][ckey][1],
                curvature_radius=c["imaging_system"]["focal_length"],
            )
            c["camera"]["centers"][ckey][2] = -1.0 * sphere_z

        for ckey in c["camera"]["centers"]:
            axis, angle = segmented_mirror.facet_rotation_axis_and_angle(
                facet_center=c["camera"]["centers"][ckey],
                target_point=c["imaging_system"]["center"],
                direction_incoming_light=np.array([0.0, 0.0, 1.0]),
            )
            if np.abs(angle) > 0.0:
                c["camera"]["rotations"][ckey] = {
                    "repr": "axis_angle",
                    "axis": axis.tolist(),
                    "angle_deg": float(np.rad2deg(angle)),
                }
            else:
                c["camera"]["rotations"][ckey] = {
                    "repr": "tait_bryan",
                    "xyz_deg": [0, 0, 0],
                }
    else:
        for ckey in c["camera"]["centers"]:
            c["camera"]["rotations"][ckey] = {
                "repr": "tait_bryan",
                "xyz_deg": [0, 0, 0],
            }
    return c


"""

def add_segmented_mirror_to_frame_in_scenery(
    frame,
    scenery,

    camera_field_of_view,
    outer_medium="vacuum",
    camera_num_photo_sensors_on_diagonal=5,
    cameras_point_towards_center_of_imaging_system=True,
    camera_surface_mirror="perfect_mirror",
    camera_surface_body="perfect_absorber",
    camera_photo_sensor_surface="perfect_absorber/rgb_12_12_12",
    camera_photo_sensor_gap=1e-3,
    camera_lens_medium="glass",
    camera_lens_fn=7,
    ref="light_field_sensor",
):

    Parameters
    ----------
    frame : dict
        A frame in the scenery.
    scenery : dict
        The scenery.
    config : dict
        The geometry of the working-surface in Sebastian's format used since
        his Master-thesis.

    ref : str
        A name to distinguish this mirror from others.
    join = os.path.join


    # camera
    # ------
    camera_ref = join(ref, "camera")
    camera_housing_inner_radius = (
        camera_field_of_view * imaging_system_focal_length
    )
    camera_housing_outer_radius = (2 / np.sqrt(3)) * camera_housing_inner_radius

    expected_imaging_system_fstop_number = (
        imaging_system_focal_length
        / imaging_system_diameter
    )

    camera_geometry = LightFieldCameraModule.make_geometry(
        housing_outer_radius=camera_housing_outer_radius,
        housing_wall_width=,
        housing_height=,
        lens_curvature_radius=,
        lens_fn=camera_lens_fn,
        photo_sensor_num_on_diagonal=,
        photo_sensor_gap=,
        photo_sensor_plane_distance=,
    )
    camera_mesh = LightFieldCameraModule.init(
        camera_geometry=camera_geometry,
        ref=camera_ref,
    )
    camera_mtl = {
        join(ref, "cam", "lens", "top"): join(ref, "lens"),
        join(ref, "cam", "lens", "bottom"): join(ref + "l"),
        join(ref, "cam", "lens", "side"): join(ref + "h"),
        join(ref, "cam", "housing", "top"): join(ref + "h"),
        join(ref, "cam", "housing", "bottom"): join(ref + "h"),
        join(ref, "cam", "housing", "outer"): join(ref + "h"),
        join(ref, "cam", "housing", "inner"): join(ref + "m"),
    }
    num_photo_sensors = len(
        camera_geometry["photo_sensor"]["grid"]["positions"]
    )
    for i in range(num_photo_sensors):
        mtlkey = join(ref, cam, "photo_sensor_{:06d}".format(i))
        camera_mtl[mtlkey] = ref + "p"

    # add objects
    # -----------
    assert camera_ref not in scenery["objects"]
    scenery["objects"][camera_ref] = camera_mesh

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

    aperture_outer_polygon = geometry.regular_polygon.make_vertices_xy(
        outer_radius=outer_radius_facet_supports, fn=fn_circle, rot=0.0,
    )

    facet_centers = init_facet_centers_xy(
        aperture_outer_polygon=aperture_outer_polygon,
        aperture_inner_polygon=geometry.regular_polygon.make_vertices_xy(
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
    camera_id = 0
    for fkey in camera_centers:
        child = {
            "id": int(camera_id),
            "pos": camera_centers[fkey],
            "rot": init_camera_rotation(
                camera_centers=camera_centers[fkey], focal_point=focal_point,
            ),
            "obj": camera_ref,
            "mtl": camera_mtl_to_boundary_layers_map,
        }
        frame["children"].append(child)
        camera_id += 1

    return scenery
"""
