import optic_object_wavefronts as oow
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as plt_Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection, Line3D
import numpy as np


def ax_add_face(
    ax, vertices, face_color="green", face_alpha=0.5, face_edge_color="black",
    face_edge_width=0.2,
):
    p = plt_Polygon(
        vertices,
        closed=False,
        facecolor=face_color,
        alpha=face_alpha,
        edgecolor=face_edge_color,
        linewidth=face_edge_width,
    )
    ax.add_patch(p)


def ax_add_object_xy(
    ax,
    obj,
    vertex_color="k",
    vertex_marker="x",
    vertex_marker_size=0.1,
    face_color="green",
    face_alpha=0.5,
    face_edge_color="black",
    face_edge_width=0.2,
):
    for vkey in obj["vertices"]:
        ax.plot(
            obj["vertices"][vkey][0],
            obj["vertices"][vkey][1],
            marker=vertex_marker,
            color=vertex_color,
            markersize=vertex_marker_size,
        )

    for fkey in obj["faces"]:
        vs = []
        for ii in range(3):
            vkey = obj["faces"][fkey]["vertices"][ii]
            vs.append(obj["vertices"][vkey][0:2])
        vs = np.array(vs)
        ax_add_face(
            ax=ax,
            vertices=vs,
            face_alpha=face_alpha,
            face_color=face_color,
            face_edge_color=face_edge_color,
            face_edge_width=face_edge_width,
        )


def plot_Object(obj):
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.set_aspect("equal")
    ax_add_object_xy(ax=ax, obj=obj)
    plt.show()


def ax_add_object_xyz(
    ax,
    obj,
    face_edge_width=1.0,
    face_edge_color="black",
    face_color="white",
    material_colors={},
    face_alpha=0.5,
    vertex_normal_color="pink",
    vertex_normal_width=0.5,
    vertex_normal_length=0.05,
    vertex_normal_alpha=1.0,
    zorder=1,
):
    wavefront = oow.Wavefront.init_from_Object(obj=obj)

    vertices = [(v[0], v[1], v[2]) for v in wavefront["v"]]

    # faces
    # -----
    polygons = []
    facecolors = []
    edgecolors = []
    linewidths = []
    for material in wavefront["materials"]:
        for face in wavefront["materials"][material]:
            polygons.append(
                [
                    vertices[face["v"][0]],
                    vertices[face["v"][1]],
                    vertices[face["v"][2]],
                ]
            )

            edgecolors.append(face_edge_color)
            linewidths.append(face_edge_width)

            if material in material_colors:
                facecolors.append(material_colors[material])
            else:
                facecolors.append(face_color)


    # normals
    # -------
    for material in wavefront["materials"]:
        for face in wavefront["materials"][material]:
            for n in range(3):
                normal =  vertex_normal_length * np.array(wavefront["vn"][face["vn"][n]])
                start = wavefront["v"][face["v"][n]]
                stop = start + normal

                polygons.append(
                    [
                        start,
                        stop,
                        stop,
                    ]
                )

                edgecolors.append(vertex_normal_color)
                linewidths.append(vertex_normal_width)
                facecolors.append("None")


    ax.add_collection3d(
        Poly3DCollection(
            polygons,
            edgecolors=edgecolors,
            facecolors=facecolors,
            linewidths=linewidths,
            alpha=face_alpha,
            zorder=zorder,
        )
    )

