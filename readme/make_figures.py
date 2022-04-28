import subprocess
import optic_object_wavefronts as oow
from optic_object_wavefronts import plot

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Every object
# ------------

# 3D
# --
objs = {
    "disc": {"outer_radius": 1.0, "fn": 109, "rot": 0.0},
    "cylinder": {"outer_radius": 1.0, "length": 0.5, "fn": 13, "rot": 0.0},
    "spherical_cap_regular": {
        "outer_radius": 1.0,
        "inner_radius": 0.2,
        "curvature_radius": 4.0,
        "fn_polygon": 31,
        "rot": 0.0,
        "fn_hex_grid": 5,
    },
    "spherical_cap_hexagonal": {
        "outer_radius": 1.0,
        "curvature_radius": 4.0,
        "fn": 5,
    },
    "spherical_cap_pixels": {
        "outer_radius": 1.0,
        "curvature_radius": 4.0,
        "fn_hex_grid": 25,
    },
    "spherical_lens": {
        "outer_radius": 1.0,
        "curvature_radius_top": 4.0,
        "curvature_radius_bot": -8.0,
        "offset": 0.25,
        "fn_polygon": 31,
        "fn_hex_grid": 17,
        "inner_radius": 0.33,
        "rot": 0.0,
        "ref": "lens",
    },
    "spherical_lens_hexagonal": {
        "outer_radius": 1.0,
        "curvature_radius": 1.5,
        "fn": 11,
        "ref": "lens",
    },
    "spherical_planar_lens_hexagonal": {
        "outer_radius": 1.0,
        "curvature_radius": 2.0,
        "fn": 11,
        "width": 0.3,
        "ref": "lens",
    },
}


for obj_key in objs:
    kwargs = objs[obj_key]
    obj = getattr(oow.objects, obj_key).init(**kwargs)

    fig, ax3d = oow.plot.fig_ax_3d(figsize=(4, 4), dpi=320)
    oow.plot.ax_add_object_3d(
        ax=ax3d, obj=obj, face_alpha=0.9, face_color="w", face_edge_width=0.3,
    )
    oow.plot.ax_aspect_equal_3d(ax=ax3d)
    ax3d.view_init(elev=30, azim=50)
    fig.savefig("{:s}.jpg".format(obj_key))

    subprocess.call(
        [
            "convert",
            "-crop",
            "640x480+340+370",
            "{:s}.jpg".format(obj_key),
            "{:s}.jpg".format(obj_key),
        ]
    )
