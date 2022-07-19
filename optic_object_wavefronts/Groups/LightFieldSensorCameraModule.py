from .. import Object
from .. import Geometry
from .. import Primitives
from .. import polygon
import numpy as np


def make_geometry(
    housing_outer_radius,
    housing_wall_width,
    housing_height,
    lens_curvature_radius,
    lens_fn,
    photo_sensor_num_on_diagonal,
    photo_sensor_gap,
    photo_sensor_plane_distance,
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

    c = {}
    c["housing"] = {}
    c["housing"]["outer_radius_outside"] = housing_outer_radius
    c["housing"]["wall_width"] = housing_wall_width
    c["housing"]["height"] = housing_height
    c["housing"]["outer_radius_inside"] = (
        c["housing"]["outer_radius_outside"] - c["housing"]["wall_width"]
    )
    c["housing"]["position"] = np.array(
        [0.0, 0.0, photo_sensor_plane_distance - c["housing"]["height"],]
    )

    c["lens"] = {}
    c["lens"]["curvature_radius"] = lens_curvature_radius
    c["lens"]["outer_radius"] = c["housing"]["outer_radius_outside"]
    c["lens"]["fn"] = lens_fn
    c["lens"]["position"] = np.array([0, 0, 0])

    c["photo_sensor"] = {}
    c["photo_sensor"]["grid"] = {}
    c["photo_sensor"]["grid"]["gap"] = photo_sensor_gap
    c["photo_sensor"]["grid"]["num_on_diagonal"] = photo_sensor_num_on_diagonal
    c["photo_sensor"]["grid"]["distance_to_lens"] = photo_sensor_plane_distance

    c["photo_sensor"]["grid"][
        "spacing"
    ] = Geometry.Grid.Hexagonal.estimate_spacing_for_small_hexagons_in_big_hexagon(
        big_hexagon_outer_radius=c["housing"]["outer_radius_inside"],
        num_small_hexagons_on_diagonal_of_big_hexagon=c["photo_sensor"][
            "grid"
        ]["num_on_diagonal"],
    )

    grid_positions_xy = Geometry.Grid.Hexagonal.init_from_spacing(
        spacing=c["photo_sensor"]["grid"]["spacing"],
        ref="_",
        fN=c["photo_sensor"]["grid"]["num_on_diagonal"],
    )
    grid_positions_xy = polygon.rotate_z(grid_positions_xy, 0)
    grid_positions_xy = polygon.get_vertices_inside(
        vertices=grid_positions_xy,
        polygon=Geometry.regular_polygon.make_vertices_xy(
            outer_radius=c["housing"]["outer_radius_inside"],
            ref="_",
            fn=6,
            rot=0,
        ),
    )
    for gkey in grid_positions_xy:
        grid_positions_xy[gkey][2] = c["photo_sensor"]["grid"][
            "distance_to_lens"
        ]
    c["photo_sensor"]["grid"]["positions"] = grid_positions_xy

    c["photo_sensor"]["bound"] = {}
    c["photo_sensor"]["bound"]["inner_radius"] = (
        1 / 2 * c["photo_sensor"]["grid"]["spacing"]
    )
    c["photo_sensor"]["bound"]["outer_radius"] = (
        2 / np.sqrt(3) * c["photo_sensor"]["bound"]["inner_radius"]
    )

    c["photo_sensor"]["body"] = {}
    c["photo_sensor"]["body"]["inner_radius"] = (
        c["photo_sensor"]["bound"]["inner_radius"]
        - 0.5 * c["photo_sensor"]["grid"]["gap"]
    )
    c["photo_sensor"]["body"]["outer_radius"] = (
        2 / np.sqrt(3) * c["photo_sensor"]["body"]["inner_radius"]
    )
    return c


def init(
    camera_geometry, ref="LightFieldSensorCameraModule",
):
    cg = camera_geometry
    camera = Object.init()

    # grid for photo-sensors
    # ----------------------
    for gi, gkey in enumerate(cg["photo_sensor"]["grid"]["positions"]):
        photo_sensor = Primitives.Disc.init(
            outer_radius=cg["photo_sensor"]["body"]["outer_radius"],
            fn=6,
            rot=np.pi / 6,
            ref=ref + "/photo_sensor_{:06d}".format(gi),
            prevent_many_faces_share_same_vertex=False,
        )
        photo_sensor = Object.translate(
            photo_sensor, cg["photo_sensor"]["grid"]["positions"][gkey],
        )
        camera = Object.merge(camera, photo_sensor)

    # lens
    # ----
    lens = Primitives.SphericalLensHexagonal.init(
        outer_radius=cg["lens"]["outer_radius"],
        curvature_radius=cg["lens"]["curvature_radius"],
        fn=cg["lens"]["fn"],
        ref=ref + "/lens",
    )
    camera = Object.merge(
        camera, Object.translate(lens, cg["lens"]["position"]),
    )

    # housing
    # -------
    pipe = Primitives.PipeHexagonal.init(
        outer_radius=cg["housing"]["outer_radius_outside"],
        inner_radius=cg["housing"]["outer_radius_inside"],
        height=cg["housing"]["height"],
        ref=ref + "/housing",
    )

    camera = Object.merge(
        camera, Object.translate(pipe, cg["housing"]["position"]),
    )

    return camera
