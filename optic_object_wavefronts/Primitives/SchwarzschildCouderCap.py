from .. import Geometry
from . import TemplateCurvedSurface
import numpy as np


def init(
    outer_polygon,
    curvature_config,
    inner_polygon=None,
    fn_hex_grid=10,
    ref="SchwartzschildCouder",
):
    return TemplateCurvedSurface.init(
        outer_polygon=outer_polygon,
        curvature_config=curvature_config,
        curvature_height_function=Geometry.SchwarzschildCouder.surface_height,
        curvature_surface_normal_function=Geometry.SchwarzschildCouder.surface_normal,
        inner_polygon=inner_polygon,
        fn_hex_grid=fn_hex_grid,
        ref=ref,
    )