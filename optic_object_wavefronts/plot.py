import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as plt_Polygon
import numpy as np


def _add_face(ax, vertices, alpha=None, color="blue"):
    p = plt_Polygon(
        vertices, closed=False, facecolor=color, alpha=alpha, edgecolor="k"
    )
    ax.add_patch(p)


def plot_Object(obj):
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.set_aspect("equal")
    for vkey in obj["vertices"]:
        ax.plot(obj["vertices"][vkey][0], obj["vertices"][vkey][1], "xb")

    for fkey in obj["faces"]:
        vs = []
        for ii in range(3):
            vkey = obj["faces"][fkey]["vertices"][ii]
            vs.append(obj["vertices"][vkey][0:2])
        vs = np.array(vs)
        _add_face(ax=ax, vertices=vs, alpha=0.5, color="green")
    plt.show()
