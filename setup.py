""" EEA Sparql Installer
"""
import os
from setuptools import setup, find_packages

NAME = 'eea.sparql'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description="Wrapper for Products.ZSPARQLMethod",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)",
        ],
      keywords='eea sparql zope plone',
      author='European Environment Agency',
      author_email='webadmin@eea.europa.eu',
      maintainer='Zoltan Szabo (Eau de Web)',
      maintainer_email='zoltan.szabo@eaudeweb.ro',
      bugtrack_url="https://github.com/eea/eea.sparql/issues",
      download_url="http://pypi.python.org/pypi/eea.sparql",
      url='https://eea.github.com/docs/eea.sparql',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.ZSPARQLMethod',
          'eea.versions'
      ],
      extras_require={
          'test': [
              'plone.app.testing',
          ]
      },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
