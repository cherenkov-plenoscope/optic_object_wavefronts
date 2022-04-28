import optic_object_wavefronts as oow


def test_min_max_distance():
    polygon = oow.Geometry.regular_polygon.make_vertices_xy(
        outer_radius=1.0, ref="ring", fn=4, rot=0.0,
    )

    point = (0.0, 0.0)
    keys, dists = oow.polygon.find_min_max_distant_to_point(
        polygon=polygon, point=point,
    )

    assert keys[0] == "('ring', 0)"
    assert dists[0] == 1.0

    assert keys[1] == "('ring', 3)"
    assert dists[1] == 1.0

    point = (0.1, 0.0)
    keys, dists = oow.polygon.find_min_max_distant_to_point(
        polygon=polygon, point=point,
    )

    assert keys[0] == "('ring', 0)"
    assert dists[0] == 0.9

    assert keys[1] == "('ring', 2)"
    assert dists[1] == 1.1
