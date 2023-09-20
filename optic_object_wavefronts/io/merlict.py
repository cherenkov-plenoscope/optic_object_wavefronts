import numpy as np
import tarfile
import io
import json_numpy
from . import obj
from .. import materials


def init(default_medium="vacuum"):
    """
    Returns a Scenery.
    A scenery is a tree of references to primitives.
    A reference is a translation and rotation to describe the object's
    relations w.r.t. each other.

    Further, the Scenery contains the materials.

    A scenery can be exported to the merlict_c89 ray-tracer.
    """
    scenery = {
        "materials": {
            "media": {},
            "surfaces": {},
            "boundary_layers": {},
            "default_medium": default_medium,
        },
        "geometry": {
            "objects": {},
            "relations": {"children": []},
        },
    }
    scenery["materials"]["media"][default_medium] = materials.medium(
        key=default_medium
    )
    return scenery


def write_to_merlict(scenery, path):
    with tarfile.open(path, mode="w") as tarout:
        # README
        # ------
        RM = "Scenery\n"
        RM += "=======\n"

        tar_append_file(
            tarout=tarout,
            file_name="README.md",
            file_bytes=str.encode(RM),
        )

        # geometry
        # --------
        tar_append_dir(tarout, "geometry")

        # objects
        tar_append_dir(tarout, "geometry/objects")
        for okey in scenery["geometry"]["objects"]:
            wfr = obj.init_from_mesh(mesh=scenery["geometry"]["objects"][okey])
            wavefront_str = obj.dumps(obj=wfr)
            tar_append_file(
                tarout=tarout,
                file_name="geometry/objects/{:s}.obj".format(okey),
                file_bytes=str.encode(wavefront_str),
            )

        # relations
        relations_json_str = json_numpy.dumps(
            scenery["geometry"]["relations"], indent=0
        )
        tar_append_file(
            tarout=tarout,
            file_name="geometry/relations.json",
            file_bytes=str.encode(relations_json_str),
        )

        # materials
        # ---------
        tar_append_dir(tarout, "materials")

        # media
        # -----
        tar_append_dir(tarout, "materials/media")
        for mkey in scenery["materials"]["media"]:
            medium_json_str = json_numpy.dumps(
                scenery["materials"]["media"][mkey],
                indent=4,
            )
            tar_append_file(
                tarout=tarout,
                file_name="materials/media/{:s}.json".format(mkey),
                file_bytes=str.encode(medium_json_str),
            )

        # surfaces
        # --------
        tar_append_dir(tarout, "materials/surfaces")
        for skey in scenery["materials"]["surfaces"]:
            surface_json_str = json_numpy.dumps(
                scenery["materials"]["surfaces"][skey],
                indent=4,
            )
            tar_append_file(
                tarout=tarout,
                file_name="materials/surfaces/{:s}.json".format(skey),
                file_bytes=str.encode(surface_json_str),
            )

        # boundary_layers
        # ---------------
        boundary_layers_json_str = json_numpy.dumps(
            scenery["materials"]["boundary_layers"],
            indent=4,
        )
        tar_append_file(
            tarout=tarout,
            file_name="materials/boundary_layers.json",
            file_bytes=str.encode(boundary_layers_json_str),
        )

        # default_medium
        # --------------
        default_medium_str = scenery["materials"]["default_medium"]
        tar_append_file(
            tarout=tarout,
            file_name="materials/default_medium.txt",
            file_bytes=str.encode(default_medium_str),
        )


def tar_append_dir(tarout, dir_name):
    info = tarfile.TarInfo(dir_name)
    info.type = tarfile.DIRTYPE
    tarout.addfile(info)


def tar_append_file(tarout, file_name, file_bytes):
    with io.BytesIO() as buff:
        info = tarfile.TarInfo(file_name)
        info.size = buff.write(file_bytes)
        buff.seek(0)
        tarout.addfile(info, buff)
