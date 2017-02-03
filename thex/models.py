"""
Database models for the Transient Host galaxy Exchange

author: Curtis McCully

February 2017
"""
from django.db import models


class HostGalaxy(models.Model):
    """
    Host galaxy object in the DB
    """
    ra = models.FloatField(default=None)
    dec = models.FloatField(default=None)
    redshift = models.FloatField(default=None)


class HostName(models.Model):
    """
    Name of a host galaxy.

    Notes
    =====
    Because host galaxies can have multiple names, their names must be their own class.
    This corresponds to its own table in the DB.
    """
    name = models.CharField(max_length=50)
    galaxy = models.ForeignKey(HostGalaxy, on_delete=models.CASCADE)


class Transient(models.Model):
    """
    Transient class for the DB
    """
    transient_types = [('SN', 'Supernova'), ('GRB', 'Gamma Ray Burst'),
                       ('TDE', 'Tidal Disruption Event'), ('Nova', 'Nova'),
                       ('AT', 'Astronomical Transient')]
    host = models.ForeignKey(HostGalaxy, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100, default=None)
    ra = models.FloatField(default=None)
    dec = models.FloatField(default=None)
    discovery_date = models.DateField(default=None)
    transient_type = models.CharField(max_length=10, choices=transient_types, default='AT')
    transient_subtype = models.CharField(max_length=100, default=None)
    peak_brightness = models.FloatField(default=None)
