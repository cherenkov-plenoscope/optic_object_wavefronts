import optic_object_wavefronts as oow
import numpy as np

def test_baker_nunn():
    # baker nunn
    n_polygon = 71
    n_hex_grid = 17
    corrector_radius = 0.508 / 2.0

    cor1 = oow.primitives.spherical_lens.make_mesh(
        outer_radius=corrector_radius,
        curvature_radius_top=-13.754,
        curvature_radius_bot=-2.589,
        offset=0.02654,
        n_polygon=n_polygon,
        n_hex_grid=n_hex_grid,
        rot=0.0,
        ref="corrector1",
    )

    cor2 = oow.primitives.spherical_lens.make_mesh(
        outer_radius=corrector_radius,
        curvature_radius_top=-2.988818,
        curvature_radius_bot=2.988818,
        offset=0.01425,
        n_polygon=n_polygon,
        n_hex_grid=n_hex_grid,
        rot=0.0,
        ref="corrector2",
    )

    cor3 = oow.primitives.spherical_lens.make_mesh(
        outer_radius=corrector_radius,
        curvature_radius_top=2.589,
        curvature_radius_bot=13.754,
        offset=0.02654,
        n_polygon=n_polygon,
        n_hex_grid=n_hex_grid,
        rot=0.0,
        ref="corrector3",
    )

    corrector = oow.Mesh.init()
    corrector = oow.Mesh.merge(
        corrector,
        oow.Mesh.translate(cor1, np.array([0.0, 0.0, 0.0]))
    )

    corrector = oow.Mesh.merge(
        corrector,
        oow.Mesh.translate(cor2, np.array([0.0, 0.0, - 1 * 0.0492]))
    )

    corrector = oow.Mesh.merge(
        corrector,
        oow.Mesh.translate(cor3, np.array([0.0, 0.0, - 2 * 0.0492 - 0.01425]))
    )

    oow.write_mesh("baker_nunn.obj", corrector)
