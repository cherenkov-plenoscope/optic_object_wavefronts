import optic_object_wavefronts as oow
import numpy as np


def test_min_max_distance():
    polygon = oow.geometry.regular_polygon.make_vertices_xy(
        outer_radius=1.0,
        ref="ring",
        fn=4,
        rot=0.0,
    )

    point = (0.0, 0.0)
    keys, dists = oow.polygon.find_min_max_distant_to_point(
        polygon=polygon,
        point=point,
    )

    assert keys[0] == "ring/000000"
    assert dists[0] == 1.0

    assert keys[1] == "ring/000003"
    assert dists[1] == 1.0

    point = (0.1, 0.0)
    keys, dists = oow.polygon.find_min_max_distant_to_point(
        polygon=polygon,
        point=point,
    )

    assert keys[0] == "ring/000000"
    assert dists[0] == 0.9

    assert keys[1] == "ring/000002"
    assert dists[1] == 1.1


def test_remove():
    first = {"a": [0.0, 0, 0], "b": [1.0, 1, 1]}
    second = {"y": [1.0, 2, 3], "x": [1.0, 1, 1], "z": [-1.0, 2, 3]}

    out = oow.polygon.remove_first_from_second_when_too_close(
        first=first,
        second=second,
        eps=1e-6,
    )

    assert len(out) == 2

    for key in out:
        assert key in second
        np.testing.assert_array_almost_equal(out[key], second[key])
