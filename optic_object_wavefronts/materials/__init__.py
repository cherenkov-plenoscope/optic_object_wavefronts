import pkg_resources
import os
import json


MATERIALS_DIR = pkg_resources.resource_filename(
    "optic_object_wavefronts", "materials"
)
SURFACES_DIR = os.path.join(MATERIALS_DIR, "surfaces")
MEDIA_DIR = os.path.join(MATERIALS_DIR, "media")


def surface(key):
    RGB = "/" in key

    basic_key = os.path.dirname(key) if RGB else key

    path = os.path.join(SURFACES_DIR, basic_key + ".json")
    with open(path, "rt") as f:
        c = json.loads(f.read())

    if RGB:
        rgb_key = os.path.basename(key)
        rgb = str.split(rgb_key, "_")
        assert rgb[0] == "rgb"
        assert len(rgb) == 4
        rgb = rgb[1:]
        c["color"] = [int(i) for i in rgb]
    return c


def medium(key):
    path = os.path.join(MEDIA_DIR, key + ".json")
    with open(path, "rt") as f:
        c = json.loads(f.read())
    return c
