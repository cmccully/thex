"""
Tools to import data from the open supernova catalog

author: Curtis McCully

January 2017
"""

from astropy.io import ascii
from thex import models
from datetime import datetime


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
        host_galaxy = models.HostGalaxy.objects.get(name=row['Host Name'])
        transient_data = {'host': host_galaxy, 'ra': row['R.A.'], 'dec': row['Dec.'],
                          'discovery_date': datetime.strptime(row['Disc. Date'], '%Y/%m/%d'),
                          'redshift': row['z'], 'transient_type': 'SN',
                          'transient_subtype': row['Type'], 'peak_brightness': row['mmax']}
        transient = models.Transient.objects.get_or_create(name=row['Name'],
                                                           defaults=transient_data)
        transient.save()
