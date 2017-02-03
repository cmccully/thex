"""
Utilities for scraping host galaxy information from NED

author: Curtis McCully

February 2017
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import time
import requests
from astropy import units
from astropy.coordinates import SkyCoord
from bs4 import BeautifulSoup

from thex import models
from thex.utils.dbs import get_host_name


def query_ned(host_galaxies):
    """
    Query NED to get host galaxy information

    :param host_galaxies: list of host galaxy names
    :return: html from NED with the table of the results

    Notes:
    ======
    This is very fragile to any changes by NED in their HTML formatting, but they do not
    have a proper API so this has to do.
    """
    url = 'https://ned.ipac.caltech.edu/cgi-bin/gmd?uplist={host_list}&delimiter=bar&' \
          'nondb=user_objname&position=ra%2Cdec&position=z&attdat=attned&gphotoms=q_value' \
          '&gphotoms=q_unc&gphotoms=ned_value&gphotoms=ned_unc&diamdat=ned_maj_dia&' \
          'distance=avg&distance=stddev_samp'

    # Format the names in the url
    url_host_names = '%0D%0A'.join([host_name_to_ned_url(host_name) for host_name in host_galaxies])

    response = requests.get(url.format(host_list=url_host_names))
    return response.content


def host_name_to_ned_url(host_name):
    """
    Convert a host name into a readable format for a NED URL.

    :param host_name: str
    :return: str
             The string to be used in the NED URL.
    """
    return host_name.name.replace('+', '%2B').replace(' ', '+')


def parse_ned_html(ned_html):
    """
    Parse the NED HTML table

    :param ned_html: html from NED query
    :return: list of dicts with parsed data

    Notes
    =====
    This is again very fragile to NED changing their HTML formatting.
    """
    soup = BeautifulSoup(ned_html)
    table = soup.find('pre')
    table.find('strong').extract()
    rows = table.contents[0].strip().split('\n')
    return [parse_ned_row(row) for row in rows]


def parse_ned_row(row):
    """
    Split a string from NED separated by the | character.

    :param row: str
                row of text from NED
    :return: dict
             contains Host Name, redshift, RA, and Dec

    Notes
    =====
    We will need to update this if we want to add more columns from the NED query.
    """
    split_row = row.split('|')
    parsed_row = {'name': split_row[0].strip(), 'redshift': float(split_row[3])}
    coordinate = SkyCoord(split_row[1], split_row[2], unit=(units.hourangle, units.deg))
    parsed_row['ra'], parsed_row['dec'] = coordinate.ra.deg, coordinate.dec.deg
    return parsed_row


def update_hosts_from_ned(galaxy_data):
    """
    Update the database given the data dictionary compiled from NED

    :param galaxy_data: dict
                        data dictionary from parse_ned_row()
    """
    for host_galaxy in galaxy_data:
        host = models.HostName.get(name=host_galaxy['name']).galaxy
        for key in host_galaxy:
            if key != 'name':
                setattr(host, key, host_galaxy[key])
        host.save()


def get_host_info_from_ned():
    """
    Main function to populate the host galaxy table using NED
    """
    # Load all of the host galaxies
    host_galaxies = models.HostGalaxy.objects.all()

    # Get the first name for each host galaxy
    host_names = [get_host_name(host_galaxy) for host_galaxy in host_galaxies]

    # In batches of 500 because of url length requirements
    for i in range((len(host_names) // 500) + 1):
        host_galaxy_batch = host_names[i * 500: (i + 1) * 500]
        # Query NED for the ra, dec, and redshift of the host galaxy
        ned_html = query_ned(host_galaxy_batch)
        # Scrape the returned html (ugh...)
        galaxy_data = parse_ned_html(ned_html)
        # Update the database
        update_hosts_from_ned(galaxy_data)
        # Sleep for 1 second because of NED's rules (ugh...)
        time.sleep(1)