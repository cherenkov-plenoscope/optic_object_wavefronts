import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as plt_Polygon
import numpy as np


def _add_face(ax, vertices, alpha=None, color="blue"):
    p = plt_Polygon(
        vertices, closed=False, facecolor=color, alpha=alpha, edgecolor="k"
    )
    ax.add_patch(p)


def plot_mesh(mesh):
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.set_aspect("equal")
    for vkey in mesh["vertices"]:
        ax.plot(mesh["vertices"][vkey][0], mesh["vertices"][vkey][1], "xb")

    for fkey in mesh["faces"]:
        vs = []
        for ii in range(3):
            vkey = mesh["faces"][fkey]["vertices"][ii]
            vs.append(mesh["vertices"][vkey][0:2])
        vs = np.array(vs)
        _add_face(ax=ax, vertices=vs, alpha=0.5, color="green")
    plt.show()
