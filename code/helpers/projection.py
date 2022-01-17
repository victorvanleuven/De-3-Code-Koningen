"""
maakt van 2d coordinaten (tuple) 3d coordinaten door een 0 toe te voegen
"""


def project_three_d(coord):
    if len(coord) == 2:
        coord += (0,)
    return coord