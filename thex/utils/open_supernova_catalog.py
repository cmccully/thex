"""
Tools to import data from the open supernova catalog

author: Curtis McCully

January 2017
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from astropy.io import ascii
from datetime import datetime
import numpy as np
from numpy import ma

from thex import models
from thex.utils import coordinates


def load_host_galaxies(csv_filename):
    """
    Load the host galaxy information from the open supernova catalog
    :param csv_filename: str
                         full path to the csv file exported from the open supernova catalog
                         host page.
    """
    host_table = ascii.read(csv_filename)
    for row in host_table:
        host_name = row['Galaxy/Cluster'][0]
        # Check if host galaxy exists
        try:
            host = models.HostName.objects.get(name=host_name).host
        except models.HostName.DoesNotExist:
            # If not, add it
            host = models.HostGalaxy()
            host.save()

        # Split the names into the names table
        for host_name in row['Galaxy/Cluster'].split(','):
            name, created = models.HostName.objects.get_or_create(name=host_name, galaxy=host)
            name.save()


def load_supernovae(csv_filename):
    """
    Load the supernovae into the DB tables from the open supernova catalog csv file
    :param csv_filename: str
                         Full path the open supernova catalog exported to csv file
    """
    transient_table = ascii.read(csv_filename)

    for row in transient_table:
        try:
            host_galaxy = models.HostName.objects.get(name=row['Host Name']).galaxy
        except models.HostName.DoesNotExist:
            host_galaxy = None
        if row['R.A.'] is ma.masked or row['Dec.'] is ma.masked:
            ra, dec = None, None
        else:
            ra, dec = coordinates.average_position(row['R.A.'].split(','), row['Dec.'].split(','))
        if row['z'] is ma.masked:
            redshift = None
        else:
            redshift = np.mean([float(z) for z in row['z'].split(',')])


        transient_data = {'host': host_galaxy, 'ra': ra, 'dec': dec,
                          'discovery_date': datetime.strptime(row['Disc. Date'], '%Y/%m/%d'),
                          'redshift': redshift, 'transient_type': 'SN',
                          'transient_subtype': row['Type'], 'peak_brightness': row['mmax']}
        transient, created = models.Transient.objects.get_or_create(name=row['Name'],
                                                                    defaults=transient_data)
        transient.save()
