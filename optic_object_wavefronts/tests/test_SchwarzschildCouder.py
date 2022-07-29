import optic_object_wavefronts as oow
from optic_object_wavefronts import plot
import numpy as np

c = {
    "M1": {
        "outer_radius": 0.9,
        "inner_radius": 0.32,
        "curvature_config": {
            "k": 0.0,
            "c": 1.0 / -4.111,
            "a1": -8.682e-10,
            "a2": 7.391e-12,
            "a3": -2.2e-18,
            "a4": 3.292e-24,
            "a5": -6.324e-30,
            "a6": 1.735e-35,
            "a7": -1.762e-41,
            "a8": 6.565e-48,
        },
        "z": 1.2944,
    },
    "M2": {
        "outer_radius": 0.45,
        "curvature_config": {
            "k": 0.0,
            "c": 1.0 / +1.089,
            "a1": -7.308e-011,
            "a2": 1.3e-010,
            "a3": -9.276e-016,
            "a4": 1.125e-021,
            "a5": 1.50e-027,
            "a6": -1.96e-034,
            "a7": -1.541e-038,
            "a8": 1.946e-044,
        },
        "z": -0.26,
    },
    "DET": {"outer_radius": 0.1, "curvature_radius": 1.06, "z": 0.0,},
}

FN_POLYGON = 71
FN_HEX_GRID = 17


def test_init():
    m1 = oow.primitives.schwarzschild_couder_cap.init(
        outer_polygon=oow.geometry.regular_polygon.make_vertices_xy(
            outer_radius=c["M1"]["outer_radius"],
            fn=FN_POLYGON,
            ref="M1_outer",
        ),
        inner_polygon=oow.geometry.regular_polygon.make_vertices_xy(
            outer_radius=c["M1"]["inner_radius"],
            fn=FN_POLYGON,
            ref="M1_inner",
        ),
        curvature_config=c["M1"]["curvature_config"],
        fn_hex_grid=FN_HEX_GRID * 2,
        ref="M1",
    )

    m2 = oow.primitives.schwarzschild_couder_cap.init(
        outer_polygon=oow.geometry.regular_polygon.make_vertices_xy(
            outer_radius=c["M2"]["outer_radius"],
            fn=FN_POLYGON,
            ref="M2_inner",
        ),
        inner_polygon=None,
        curvature_config=c["M2"]["curvature_config"],
        fn_hex_grid=FN_HEX_GRID,
        ref="M2",
    )

    det = oow.primitives.spherical_cap.init(
        outer_polygon=oow.geometry.regular_polygon.make_vertices_xy(
            outer_radius=c["DET"]["outer_radius"],
            fn=FN_POLYGON,
            ref="DET_outer",
        ),
        curvature_radius=c["DET"]["curvature_radius"],
        ref="DET",
        fn_hex_grid=FN_HEX_GRID // 3,
    )

    telescope = oow.mesh.init()

    telescope = oow.mesh.merge(
        telescope, oow.mesh.translate(m1, np.array([0.0, 0.0, c["M1"]["z"]])),
    )

    telescope = oow.mesh.merge(
        telescope, oow.mesh.translate(m2, np.array([0.0, 0.0, c["M2"]["z"]])),
    )

    telescope = oow.mesh.merge(
        telescope,
        oow.mesh.translate(det, np.array([0.0, 0.0, c["DET"]["z"]])),
    )

    oow.mesh.write_to_obj(mesh=telescope, path="tiny_telescope.obj")

    fig, ax3d = oow.plot.fig_ax_3d(figsize=(10, 10), dpi=320)
    oow.plot.ax_add_mesh_3d(
        ax=ax3d,
        mesh=telescope,
        face_alpha=0.9,
        face_color="w",
        face_edge_width=0.3,
    )
    oow.plot.ax_aspect_equal_3d(ax=ax3d)
    ax3d.view_init(elev=30, azim=50)
    fig.savefig("tiny_telescope.jpg")
