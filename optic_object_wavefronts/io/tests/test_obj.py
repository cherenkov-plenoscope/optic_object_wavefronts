import optic_object_wavefronts as oow
import tempfile
import os


def test_oby_io():
    my_thing_mesh = oow.primitives.spherical_lens.init(
        outer_radius=0.508 / 2.0,
        curvature_radius_top=-13.754,
        curvature_radius_bot=-2.589,
        offset=0.02654,
        fn_polygon=71,
        fn_hex_grid=17,
        rot=0.0,
        ref="my_thing",
    )

    with tempfile.TemporaryDirectory(prefix="optic_object_wavefronts_") as tmp:
        tmp_path = os.path.join(tmp, "my_thing.obj")

        my_thing_obj = oow.io.reduce_mesh_to_obj(my_thing_mesh)

        with open(tmp_path, "wt") as f:
            f.write(oow.io.obj.dumps(my_thing_obj))

        with open(tmp_path, "rt") as f:
            my_thing_obj_back = oow.io.obj.loads(f.read())

        diff = oow.io.obj.diff(my_thing_obj, my_thing_obj_back)

        if diff:
            print(diff)
        assert len(diff) == 0

    my_thing_mesh_back = oow.io.restore_mesh_from_obj(my_thing_obj_back)
    my_thing_obj_back_back = oow.io.reduce_mesh_to_obj(my_thing_mesh_back)

    diff = oow.io.obj.diff(my_thing_obj, my_thing_obj_back_back)

    if diff:
        print(diff)
    assert len(diff) == 0
