from setuptools import setup, find_packages
import sys, os

version = '0.1.15'
long_description = ""

setup(name='netflowindexer',
      version=version,
      description="Index netflow",
      long_description=long_description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='netflow search index',
      author='Justin Azoff',
      author_email='JAzoff@uamail.albany.edu',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points = {
        'console_scripts': [
            'netflow-index-update     = netflowindexer.main:index',
            'netflow-index-search     = netflowindexer.main:search',
            'netflow-index-search-all = netflowindexer.main:search_all',
            'netflow-index-cleanup    = netflowindexer.main:cleanup',
        ]
      }
  )
