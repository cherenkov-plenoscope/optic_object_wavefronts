import optic_object_wavefronts as oow
import numpy as np

def test_baker_nunn():
    # baker nunn
    n_polygon = 71
    n_hex_grid = 17

    corrector_radius = 0.508 / 2.0
    mirror_radius = 0.7600 / 2.0
    mirror_curvature_radius = 1.016167
    mirror_thickness = 0.05

    mirr_to_corr3 = 0.9448
    corr3_width = 0.02654
    corr1_width = corr3_width
    corr2_width = 0.01425
    corr3_to_corr2 = 0.0492
    corr2_to_corr1 = corr3_to_corr2

    z_mirror = 0.0
    z_corr3 = mirr_to_corr3 + corr3_width
    z_corr2 = z_corr3 + corr3_to_corr2 + corr2_width
    z_corr1 = z_corr2 + corr2_to_corr1 + corr1_width

    mirror = oow.primitives.spherical_lens.make_mesh(
        outer_radius=mirror_radius,
        inner_radius=0.0254,
        curvature_radius_top=-mirror_curvature_radius,
        curvature_radius_bot=-mirror_curvature_radius - mirror_thickness,
        offset=mirror_thickness,
        n_polygon=n_polygon,
        n_hex_grid=n_hex_grid,
        rot=0.0,
        ref="mirror",
    )

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

    baker_nunn = oow.Mesh.init()

    baker_nunn = oow.Mesh.merge(
        baker_nunn,
        oow.Mesh.translate(mirror, np.array([0.0, 0.0, z_mirror]))
    )

    baker_nunn = oow.Mesh.merge(
        baker_nunn,
        oow.Mesh.translate(cor3, np.array([0.0, 0.0, z_corr3]))
    )


    baker_nunn = oow.Mesh.merge(
        baker_nunn,
        oow.Mesh.translate(cor2, np.array([0.0, 0.0, z_corr2]))
    )

    baker_nunn = oow.Mesh.merge(
        baker_nunn,
        oow.Mesh.translate(cor1, np.array([0.0, 0.0, z_corr1]))
    )

    oow.write_mesh("baker_nunn.obj", baker_nunn)
