"""
Tests for db utility functions

author: Curtis McCully

February 2017
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from django.test import TestCase
from thex.utils import dbs
from thex import models


class DBUtilsTestCase(TestCase):
    def setUp(self):
        host1 = models.HostGalaxy.objects.create()
        models.HostName.objects.create(name='test1', galaxy=host1)
        models.HostName.objects.create(name='testgal1', galaxy=host1)

        host2 = models.HostGalaxy.objects.create()
        models.HostName.objects.create(name='test2', galaxy=host2)

    def test_get_host_name(self):
        host1 = models.HostName.objects.get(name='testgal1').galaxy
        self.assertEqual(dbs.get_host_name(host1), 'test1')
        host2 = models.HostName.objects.get(name='test2').galaxy
        self.assertEqual(dbs.get_host_name(host2), 'test2')
