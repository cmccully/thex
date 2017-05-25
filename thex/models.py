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
    ra = models.FloatField(default=None, null=True)
    dec = models.FloatField(default=None, null=True)
    redshift = models.FloatField(default=None, null=True)


class HostName(models.Model):
    """
    Name of a host galaxy.

    Notes
    =====
    Because host galaxies can have multiple names, their names must be their own class.
    This corresponds to its own table in the DB.
    """
    name = models.CharField(max_length=50, default=None)
    galaxy = models.ForeignKey(HostGalaxy, on_delete=models.CASCADE, default=None)


class Transient(models.Model):
    """
    Transient class for the DB
    """
    transient_types = [('SN', 'Supernova'), ('GRB', 'Gamma Ray Burst'),
                       ('TDE', 'Tidal Disruption Event'), ('Nova', 'Nova'),
                       ('AT', 'Astronomical Transient')]
    host = models.ForeignKey(HostGalaxy, on_delete=models.CASCADE, default=None, null=True)
    name = models.CharField(max_length=100)
    ra = models.FloatField(default=None, null=True)
    dec = models.FloatField(default=None, null=True)
    redshift = models.FloatField(default=None, null=True)
    discovery_date = models.DateField(default=None, null=True)
    transient_type = models.CharField(max_length=10, choices=transient_types, default='AT')
    transient_subtype = models.CharField(max_length=100, default=None, null=True)
    peak_brightness = models.FloatField(default=None, null=True)
