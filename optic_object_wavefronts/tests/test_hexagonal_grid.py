import optic_object_wavefronts as oow
import numpy as np


def test_grid_vertices():
    vs = oow.geometry.hexagonal_grid.make_vertices_xy(
        outer_radius=8.0, fn=10, ref="abc"
    )
    np.testing.assert_array_equal([vs[k][2] for k in vs], 0.0)
    np.testing.assert_almost_equal(np.min([vs[k][0] for k in vs]), -8.0)
    np.testing.assert_almost_equal(np.max([vs[k][0] for k in vs]), 8.0)


def test_grid_vertices_num():
    vs = oow.geometry.hexagonal_grid.make_vertices_xy(
        outer_radius=1.0, fn=1, ref="abc"
    )
    assert len(vs) == 6 + 1


def test_grid_vertices_ref():
    vs = oow.geometry.hexagonal_grid.make_vertices_xy(
        outer_radius=1.0, fn=1, ref="abc"
    )
    for k in vs:
        assert k[0] == "abc"
