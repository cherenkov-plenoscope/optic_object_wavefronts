from .. import Object
from .. import Geometry
from .. import Primitives
from .. import Polygon
import numpy as np


def init(
    housing_outer_radius,
    housing_wall_width,
    housing_height,
    lens_curvature_radius,
    lens_fn,
    photo_sensor_num_on_diagonal,
    photo_sensor_gap,
    photo_sensor_plane_distance,
    ref="LightFieldSensorCameraModule",
):
    """
    Parameters
    ----------
    housing_outer_radius : float
        Outer radius of hexagonal housing.
    housing_wall_width : float
        Width of walls of housing.
    housing_height
        Height of housung.
    lens_curvature_radius : float
        Curvature radius of biconvex lens. Same curvature on both sides.
    lens_fn : int
        Resolution of lens.
    photo_sensor_num_on_diagonal : int
        Number of photo-sensors on the long diagonal insisde the hexagonal
        housing.
    photo_sensor_gap : float
        Gap between photo-sensors.
    photo_sensor_plane_distance : float
        Distance from lens'
    ref : str
        Name to reference multiple modules.
    """
    assert housing_outer_radius > 0.0
    assert housing_wall_width > 0.0
    assert housing_height > 0.0
    assert photo_sensor_plane_distance > 0.0
    assert housing_height <= photo_sensor_plane_distance

    assert lens_fn > 0
    assert lens_curvature_radius > 0.0
    assert photo_sensor_gap >= 0.0

    camera = Object.init()

    # grid for photo-sensors
    # ----------------------
    outer_radius_of_hexagon_to_fit_all_sensors_in = (
        housing_outer_radius - housing_wall_width
    )

    photo_sensor_spacing = Geometry.Grid.Hexagonal.estimate_spacing_for_small_hexagons_in_big_hexagon(
        big_hexagon_outer_radius=outer_radius_of_hexagon_to_fit_all_sensors_in,
        num_small_hexagons_on_diagonal_of_big_hexagon=photo_sensor_num_on_diagonal,
    )

    photo_sensor_bound_inner_radius = 1 / 2 * photo_sensor_spacing
    photo_sensor_inner_radius = (
        photo_sensor_bound_inner_radius - 0.5 * photo_sensor_gap
    )
    photo_sensor_outer_radius = 2 / np.sqrt(3) * photo_sensor_inner_radius

    photo_sensors_centers_xy = Geometry.Grid.Hexagonal.init_from_spacing(
        spacing=photo_sensor_spacing, ref="_", fN=photo_sensor_num_on_diagonal,
    )
    photo_sensors_centers_xy = Polygon.rotate_z(photo_sensors_centers_xy, 0)
    photo_sensors_centers_xy = Polygon.get_vertices_inside(
        vertices=photo_sensors_centers_xy,
        polygon=Geometry.RegularPolygon.make_vertices_xy(
            outer_radius=(housing_outer_radius - housing_wall_width),
            ref="_",
            fn=6,
            rot=0,
        ),
    )

    for ipsc, psckey in enumerate(photo_sensors_centers_xy):
        photo_sensor = Primitives.Disc.init(
            outer_radius=photo_sensor_outer_radius,
            fn=6,
            rot=np.pi / 6,
            ref=ref + "/photo_sensor_{:06d}".format(ipsc),
            prevent_many_faces_share_same_vertex=False,
        )

        shift_xy = photo_sensors_centers_xy[psckey]
        shift_z = np.array([0.0, 0.0, photo_sensor_plane_distance])
        shift_xyz = shift_xy + shift_z
        photo_sensor = Object.translate(photo_sensor, shift_xyz)
        camera = Object.merge(camera, photo_sensor)

    # lens
    # ----
    lens = Primitives.SphericalLensHexagonal.init(
        outer_radius=housing_outer_radius,
        curvature_radius=lens_curvature_radius,
        fn=lens_fn,
        ref=ref + "/lens",
    )
    camera = Object.merge(camera, Object.translate(lens, [0.0, 0.0, 0.0]),)

    # housing
    # -------
    pipe = Primitives.PipeHexagonal.init(
        outer_radius=housing_outer_radius,
        inner_radius=housing_outer_radius - housing_wall_width,
        height=housing_height,
        ref=ref + "/housing",
    )

    camera = Object.merge(
        camera,
        Object.translate(
            pipe, [0.0, 0.0, photo_sensor_plane_distance - housing_height]
        ),
    )

    return camera
