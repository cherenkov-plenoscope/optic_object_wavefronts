import subprocess
import optic_object_wavefronts as oow
from optic_object_wavefronts import plot

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as plt_colors


def my_fig_ax():
    fig = plt.figure(figsize=(4, 4), dpi=160)
    ax = fig.add_axes([0.0, 0.0, 1, 1])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_aspect("equal")
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    return fig, ax


def my_fig_ax_3d():
    fig = plt.figure(figsize=(4, 4), dpi=320)
    ax = fig.add_subplot(111, projection="3d")
    ax.grid(False)
    ax.axes.set_xlim3d(left=-1, right=1)
    ax.axes.set_ylim3d(bottom=-1, top=1)
    ax.axes.set_zlim3d(bottom=-1, top=1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    return fig, ax


def ax_aspect_equal_3d(ax):
    extents = np.array(
        [getattr(ax, "get_{}lim".format(dim))() for dim in "xyz"]
    )
    sz = extents[:, 1] - extents[:, 0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize / 2
    for ctr, dim in zip(centers, "xyz"):
        getattr(ax, "set_{}lim".format(dim))(ctr - r, ctr + r)


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

    fig, ax = my_fig_ax_3d()
    oow.plot.ax_add_object_xyz(
        ax=ax, obj=obj, face_alpha=0.9, face_color="w", face_edge_width=0.3,
    )
    ax_aspect_equal_3d(ax=ax)
    ax.view_init(elev=30, azim=50)
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
