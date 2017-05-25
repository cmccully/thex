from astropy.coordinates import Angle
from astropy import units
import numpy as np


def average_position(ra_list, dec_list):
    ras_in_degrees = [Angle(ra, unit=units.hourangle).deg for ra in ra_list]
    decs_in_degrees = [Angle(dec, unit=units.deg).deg for dec in dec_list]
    return np.mean(ras_in_degrees), np.mean(decs_in_degrees)
