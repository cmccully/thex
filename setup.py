"""
Transient Host Exchange

An interface to collate and interact with transient host galaxy information

author: Curtis McCully (cmccully@lco.global)

January 2017
"""
from setuptools import setup

setup(name='thex',
      author=['Curtis McCully'],
      author_email=['cmccully@lco.global'],
      version=0.1,
      packages=['thex'],
      setup_requires=[],
      install_requires=['numpy', 'astropy', 'django', 'beautifulsoup4', 'requests'],
      tests_require=[])
