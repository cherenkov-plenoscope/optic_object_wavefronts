import optic_object_wavefronts as oow
import pkg_resources
import os
import tempfile


STL_PATH = pkg_resources.resource_filename(
    package_or_requirement="optic_object_wavefronts",
    resource_name=os.path.join(
        "io", "tests", "resources", "gridfinity_cup_modules_x1-y1-z5.stl"
    ),
)


def test_is_almost_equal():
    with open(STL_PATH, "rt") as f:
        a = oow.io.stl.loads(f.read(), mode="ascii")

    assert not oow.io.stl.diff(a=a, b=a)
    b = a.copy()
    b["normal.x"][1337] += 2e-6
    assert oow.io.stl.diff(a=a, b=b, eps=1e-6)
    assert not oow.io.stl.diff(a=a, b=b, eps=1e-3)


def test_read_stl():
    with open(STL_PATH, "rt") as f:
        s_orig = oow.io.stl.loads(f.read(), mode="ascii")

    with tempfile.TemporaryDirectory(prefix="triangle_mesh_io_") as tmpdir:
        tmp_ascii_path = os.path.join(tmpdir, "pot.ascii.stl")
        tmp_binary_path = os.path.join(tmpdir, "pot.binary.stl")

        with open(tmp_ascii_path, "wt") as f:
            f.write(oow.io.stl.dumps(s_orig, mode="ascii"))

        with open(tmp_ascii_path, "rt") as f:
            s_orig_to_ascii = oow.io.stl.loads(f.read(), mode="ascii")

        diff = oow.io.stl.diff(a=s_orig, b=s_orig_to_ascii, eps=1e-6)
        if diff:
            print(diff)
        assert len(diff) == 0

        with open(tmp_binary_path, "wb") as f:
            f.write(oow.io.stl.dumps(s_orig_to_ascii, mode="binary"))

        with open(tmp_binary_path, "rb") as f:
            s_orig_to_ascii_to_binary = oow.io.stl.loads(
                f.read(), mode="binary"
            )

        diff = oow.io.stl.diff(a=s_orig, b=s_orig_to_ascii_to_binary, eps=1e-6)
        if diff:
            print(diff)
        assert len(diff) == 0
