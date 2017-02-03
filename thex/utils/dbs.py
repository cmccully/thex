"""
Database utilities for THEx

author: Curtis McCully

February 2017
"""
from thex import models


def get_host_name(host_galaxy):
    """
    Given a host galaxy object, get its host name

    :param host_galaxy: HostGalaxy
    :return: str
             The first name in the DB for the given host galaxy
    """
    return models.HostName.objects.filter(galaxy=host_galaxy).first()
