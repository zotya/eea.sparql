#  EEA Sparql

[![http://ci.eionet.europa.eu/job/eea.sparql-
www/badge/icon](https://camo.githubusercontent.com/96242bc5a3e7bb6d2efd2c6f366ce7d715a073de/687474703a2f2f63692e65696f6e65742e6575726f70612e65752f6a6f622f6565612e73706172716c2d7777772f62616467652f69636f6e)](http://ci.eionet.europa.eu/job/eea
.sparql-www/lastBuild) [![http://ci.eionet.europa.eu/job/eea.sparql-
plone4/badge/icon](https://camo.githubusercontent.com/491c1568f2f1ba7e9262da828e2486a37079d951/687474703a2f2f63692e65696f6e65742e6575726f70612e65752f6a6f622f6565612e73706172716c2d706c6f6e65342f62616467652f69636f6e)](http://ci.eionet.europa.eu/job/eea
.sparql-plone4/lastBuild)

EEA Sparql is a plone product for fetching data from Linked open data servers
(sparql endpoints).

Contents

  * Introduction
  * Main features
  * Installation
  * Dependecies
  * Source code
  * Copyright and license
  * Links
  * Funding

##  Introduction

It is simple to use, you only have to specify the sparql endpoint url and the
sparql query. The results will be converted in an exhibit json, what can
easily be reused (ex. by eea.daviz).

##  Main features

The main features are:

  1. create sparql queries
  2. create sparql bookmark folders, sparql queries are created automatically, and can be synchronized manually or automatically (with a cronjob). If a query is changed, a new version of the object is created, so older ones are not lost.
  3. results are downloadable in various formats: JSON, Exhibit JSON, HTML, XML, XML with Schema, CSV, TSV

##  Installation

To install eea.sparql into the global Python environment (or a workingenv),
using a traditional Zope 2 instance, you can do this:

  * When you're reading this you have probably already run `easy_install eea.sparql`. Find out how to install setuptools (and EasyInstall) here: <http://peak.telecommunity.com/DevCenter/EasyInstall>

  * If you are using Zope 2.9 (not 2.10), get [pythonproducts](http://plone.org/products/pythonproducts) and install it via:
    
        python setup.py install --home /path/to/instance
    

into your Zope instance.

  * Create a file called `eea.sparql-configure.zcml` in the `/path/to/instance/etc/package-includes` directory. The file should only contain this:
    
        <include package="eea.sparql" />
    

Alternatively, if you are using zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, you can do this:

  * Add `eea.sparql` to the list of eggs to install, e.g.:
    
        [buildout]
    eggs = eea.sparql
    

  * Tell the plone.recipe.zope2instance recipe to install a ZCML slug:
    
        [instance]
    recipe = plone.recipe.zope2instance
    zcml = eea.sparql
    

You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.

You will also need a worker instance to be set up. This is required for the
async update of the last working results.

  * For both, normal and worker instances, the plone.app.async should be added in the EGG slug:
    
        eggs =
      ...
      plone.app.async
    

  * For the normal instances, the plone.app.async-single_db_instance should be added in the ZCML slug:
    
        zcml =
      ...
      plone.app.async-single_db_instance
    

  * For the worker instances, the plone.app.async-single_db_worker should be added in the ZCML slug:
    
        zcml =
      ...
      plone.app.async-single_db_worker
    

  * Re-run buildout, e.g. with:
    
        $ ./bin/buildout
    

##  Dependecies

  * Products.ZSPARQLMethod
  * eea.versions
  * plone.app.async
  * eea.cache 7.0+ (optional)

##  Source code

Latest source code (Plone 4 compatible): \- [Plone Collective on
Github](https://github.com/collective/eea.sparql) \- [EEA on
Github](https://github.com/eea/eea.sparql)

##  Copyright and license

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA Sparql (the Original Code) is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

More details under docs/License.txt

##  Links

  1. <http://en.wikipedia.org/wiki/SPARQL>
  2. <http://sparql.org/>
  3. <http://www.w3.org/TR/rdf-sparql-query/>

##  Funding

[EEA](http://www.eea.europa.eu/) \- European Environment Agency (EU)

