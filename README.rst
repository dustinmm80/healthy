healthy
===========

healthy checks the health of a Python package from its pypi listing

.. image:: https://api.travis-ci.org/dustinmm80/healthy.png
    :target: https://travis-ci.org/dustinmm80/healthy

The package is given a score, based on this formula: ::

    Starting score                      = 100
    No license                          - 20
    No release files                    - 20
    No download url/homepage            - 10
    No updates in a year                - 15
    No updates in 6 months              - 10 (not deducted if year penalty has already been applied)
    No summary                          - 10
    No description                      - 10
    No author name or email             - 10
    No Python compatibility classifiers - 10

Results are color coded, based on the score

Usage
-----

The simplest command you can run is ::

    healthy Flask

This will check the latest version of Flask, and give you back its score.

To check a specific version of a package with verbose output ::

    healthy Flask 0.8 -v

There are 3 optional parameters ::

    package_version     : positional, to check the health of a specific version of a package
    -v, --verbose       : show reasons for the health scores the packages were given
    -n, --no-output     : print no output to the terminal, useful for integrating healthy with other packages


Sample Output
-------------

::

    healthy Django 1.2.1 -v

    Django v1.2.1
    -----
    score: 45
    No License
    Description is missing
    Python classifiers missing
    Package not updated in 360 days

Use Case
--------

``healthy`` can be used when you are trying to choose a package from a number of options. With ``healthy`` you can
quickly gauge the risk and benefit of one package over the other and make your decision easier.

Installation
------------
::

    pip install healthy

----

Supports Python 2.7, 3.2, 3.3

Python <=2.6, 3.0 and 3.1 are not supported, they don't have argparse
