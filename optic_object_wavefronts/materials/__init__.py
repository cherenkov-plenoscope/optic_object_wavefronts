import pkg_resources
import os
import json


MATERIALS_DIR = pkg_resources.resource_filename(
    "optic_object_wavefronts", "materials"
)
SURFACES_DIR = os.path.join(MATERIALS_DIR, "surfaces")
MEDIA_DIR = os.path.join(MATERIALS_DIR, "media")


def surface(key):
    path = os.path.join(SURFACES_DIR, key + ".json")
    with open(path, "rt") as f:
        c = json.loads(f.read())
    return c


def medium(key):
    path = os.path.join(MEDIA_DIR, key + ".json")
    with open(path, "rt") as f:
        c = json.loads(f.read())
    return c
