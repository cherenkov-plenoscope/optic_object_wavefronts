import optic_object_wavefronts as oow
import triangle_mesh_io as tmi
import numpy as np
import posixpath
import collections


def test_baker_nunn():
    # baker nunn
    fn_polygon = 71
    fn_hex_grid = 17

    corrector_radius = 0.508 / 2.0
    mirror_radius = 0.7600 / 2.0
    mirror_curvature_radius = 1.016167
    mirror_thickness = 0.05

    focus_surface_curvature_radius = 0.5 * mirror_curvature_radius
    focus_surface_height = 0.05
    focus_surface_width = 0.30

    focus_shield_to_focus_surface = 0.01
    focus_shield_curvature_radius = (
        focus_surface_curvature_radius - focus_shield_to_focus_surface
    )
    focus_shield_height = focus_surface_height + 0.01
    focus_shield_width = focus_surface_width + 0.01

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

    z_focus_shield = (
        z_mirror
        + focus_surface_curvature_radius
        + focus_shield_to_focus_surface
    )
    z_focus_surfcae = z_mirror + focus_surface_curvature_radius

    mirror = oow.primitives.spherical_lens.init(
        outer_radius=mirror_radius,
        inner_radius=0.0254,
        curvature_radius_top=-mirror_curvature_radius,
        curvature_radius_bot=-mirror_curvature_radius - mirror_thickness,
        offset=mirror_thickness,
        fn_polygon=fn_polygon,
        fn_hex_grid=fn_hex_grid,
        rot=0.0,
        ref="mirror",
    )

    cor1 = oow.primitives.spherical_lens.init(
        outer_radius=corrector_radius,
        curvature_radius_top=-13.754,
        curvature_radius_bot=-2.589,
        offset=0.02654,
        fn_polygon=fn_polygon,
        fn_hex_grid=fn_hex_grid,
        rot=0.0,
        ref="corrector1",
    )

    cor2 = oow.primitives.spherical_lens.init(
        outer_radius=corrector_radius,
        curvature_radius_top=-2.988818,
        curvature_radius_bot=2.988818,
        offset=0.01425,
        fn_polygon=fn_polygon,
        fn_hex_grid=fn_hex_grid,
        rot=0.0,
        ref="corrector2",
    )

    cor3 = oow.primitives.spherical_lens.init(
        outer_radius=corrector_radius,
        curvature_radius_top=2.589,
        curvature_radius_bot=13.754,
        offset=0.02654,
        fn_polygon=fn_polygon,
        fn_hex_grid=fn_hex_grid,
        rot=0.0,
        ref="corrector3",
    )

    # focus-surface
    focus_surface_bound = collections.OrderedDict()
    focus_surface_bound[posixpath.join("f_srf", "000000")] = [
        focus_surface_width / 2,
        focus_surface_height / 2,
        0.0,
    ]
    focus_surface_bound[posixpath.join("f_srf", "000001")] = [
        -focus_surface_width / 2,
        focus_surface_height / 2,
        0.0,
    ]
    focus_surface_bound[posixpath.join("f_srf", "000002")] = [
        -focus_surface_width / 2,
        -focus_surface_height / 2,
        0.0,
    ]
    focus_surface_bound[posixpath.join("f_srf", "000003")] = [
        focus_surface_width / 2,
        -focus_surface_height / 2,
        0.0,
    ]

    focus_shield_bound = collections.OrderedDict()
    focus_shield_bound[posixpath.join("f_shi", "000000")] = [
        focus_shield_width / 2,
        focus_shield_height / 2,
        0.0,
    ]
    focus_shield_bound[posixpath.join("f_shi", "000001")] = [
        -focus_shield_width / 2,
        focus_shield_height / 2,
        0.0,
    ]
    focus_shield_bound[posixpath.join("f_shi", "000002")] = [
        -focus_shield_width / 2,
        -focus_shield_height / 2,
        0.0,
    ]
    focus_shield_bound[posixpath.join("f_shi", "000003")] = [
        focus_shield_width / 2,
        -focus_shield_height / 2,
        0.0,
    ]

    f_shield = oow.primitives.spherical_cap.init(
        outer_polygon=focus_shield_bound,
        curvature_radius=focus_shield_curvature_radius,
        fn_hex_grid=fn_hex_grid,
        ref="focus_shield",
    )
    f_surface = oow.primitives.spherical_cap.init(
        outer_polygon=focus_surface_bound,
        curvature_radius=focus_surface_curvature_radius,
        fn_hex_grid=3 * fn_hex_grid,
        ref="focus_surface",
    )

    baker_nunn = oow.mesh.init()

    baker_nunn = oow.mesh.merge(
        baker_nunn,
        oow.mesh.translate(mirror, np.array([0.0, 0.0, z_mirror])),
    )

    baker_nunn = oow.mesh.merge(
        baker_nunn, oow.mesh.translate(cor3, np.array([0.0, 0.0, z_corr3]))
    )

    baker_nunn = oow.mesh.merge(
        baker_nunn, oow.mesh.translate(cor2, np.array([0.0, 0.0, z_corr2]))
    )

    baker_nunn = oow.mesh.merge(
        baker_nunn, oow.mesh.translate(cor1, np.array([0.0, 0.0, z_corr1]))
    )

    baker_nunn = oow.mesh.merge(
        baker_nunn,
        oow.mesh.translate(
            f_shield, np.array([0.0, 0.0, z_focus_shield + 0.02])
        ),
    )

    baker_nunn = oow.mesh.merge(
        baker_nunn,
        oow.mesh.translate(f_surface, np.array([0.0, 0.0, z_focus_surfcae])),
    )

    with open("baker_nunn.obj", "wt") as f:
        bake_nunn_obj = oow.export.reduce_mesh_to_obj(baker_nunn)
        f.write(tmi.obj.dumps(bake_nunn_obj))
