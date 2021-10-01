import optic_object_wavefronts as oow
import numpy as np

def _relative(actual, expected):
    return np.abs(actual - expected) / expected


def test_sebastians_paper_pen_calculation_curvature_radius():
    expected_curvature_radius = 0.125
    curvature_radius = oow.optics.lens_maker.estimate_curvature_radius(
        focal_length=0.1335,
        aperture_radius=0.071,
        refractive_index=1.49,
    )
    assert _relative(curvature_radius, expected_curvature_radius) < 3e-2


def test_sebastians_paper_pen_calculation_thickness():
    curvature_radius = 0.125
    expected_thickness = 0.0445
    thickness = oow.optics.lens_maker.estimate_thickness(
        curvature_radius=curvature_radius,
        aperture_radius=0.071,
    )
    assert _relative(thickness, expected_thickness) < 3e-2
