from . import Ellipse


def surface_height(x, y, focal_length):
    return Ellipse.surface_height(
        x=x, y=y, focal_length_x=focal_length, focal_length_y=focal_length
    )


def surface_normal(x, y, focal_length):
    return Ellipse.surface_normal(
        x=x, y=y, focal_length_x=focal_length, focal_length_y=focal_length
    )
