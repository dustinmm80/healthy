#! /usr/bin/env python
# coding=utf-8

"""
healthy.py

Checks the health of a Python package, based on this calculation:

Health is on a scale from 0-100
"""
import argparse
from datetime import datetime, timedelta
import os

try:
    # Different location in Python 3
    from xmlrpc.client import ServerProxy
except ImportError:
    from xmlrpclib import ServerProxy

from blessings import Terminal

TERMINAL = Terminal()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CLIENT = ServerProxy('http://pypi.python.org/pypi')

DAYS_STALE = 180  # number of days without update that a package is considered 'stale'
DAYS_VERY_STALE = 360  # number of days without update that a package is considered 'very stale'

# Penalties
LICENSE_PENALTY = 20
NO_RELEASE_FILES_PENALTY = 20
VERY_STALE_PENALTY = 15
SUMMARY_PENALTY = 10
DESCRIPTION_PENALTY = 10
PYTHON_CLASSIFIERS_PENALTY = 10
AUTHOR_MISSING = 10
STALE_PENALTY = 10
DOWNLOAD_URL_PENALTY = 10

BAD_VALUES = ['UNKNOWN', '', None]


def calculate_health(package_name, package_version=None, verbose=False, no_output=False):
    """
    Calculates the health of a package, based on several factors

    :param package_name: name of package on pypi.python.org
    :param package_version: version number of package to check, optional - defaults to latest version
    :param verbose: flag to print out reasons
    :param no_output: print no output

    :returns: (score: integer, reasons: list of reasons for score)
    :rtype: tuple
    """
    score = 100
    reasons = []

    package_releases = CLIENT.package_releases(package_name)
    if not package_releases:
        if not no_output:
            print(TERMINAL.red('{} is not listed on pypi'.format(package_name)))
        return 0, []

    if package_version is None:
        package_version = package_releases[0]

    package_info = CLIENT.release_data(package_name, package_version)

    if not no_output:
        print(TERMINAL.bold('{} v{}'.format(package_name, package_version)))
        print('-----')

    try:
        package_uploaded_time = CLIENT.release_urls(package_name, package_version)[0]['upload_time']
    except Exception as e:
        package_uploaded_time = -1

    # package doesn't have a license
    if package_info.get('license') in BAD_VALUES:
        score -= LICENSE_PENALTY
        reasons.append('No License')

    # download_url or home_page missing
    if package_info.get('download_url') in BAD_VALUES and package_info.get('home_page') in BAD_VALUES:
        score -= DOWNLOAD_URL_PENALTY
        reasons.append('Download url and home page missing')

    # summary is missing
    if package_info.get('summary') in BAD_VALUES:
        score -= SUMMARY_PENALTY
        reasons.append('Summary is missing')

    # long description is missing
    if package_info.get('description') in BAD_VALUES:
        score -= DESCRIPTION_PENALTY
        reasons.append('Description is missing')

    # python classifiers missing
    classifiers = package_info.get('classifiers')
    if len([c for c in classifiers if c.startswith('Programming Language :: Python ::')]) == 0:
        score -= PYTHON_CLASSIFIERS_PENALTY
        reasons.append('Python classifiers missing')

    if package_info.get('author') in BAD_VALUES or package_info.get('author_email') in BAD_VALUES:
        score -= AUTHOR_MISSING
        reasons.append('Author name and email missing')

    if isinstance(package_uploaded_time, int) and package_uploaded_time < 0:
        score -= NO_RELEASE_FILES_PENALTY
        reasons.append('No release files have been uploaded')
    else:
        now = datetime.utcnow()

        if now - timedelta(days=DAYS_VERY_STALE) > package_uploaded_time:
            score -= VERY_STALE_PENALTY
            reasons.append('Package not updated in {} days'.format(DAYS_VERY_STALE))
        elif now - timedelta(days=DAYS_STALE) > package_uploaded_time:
            score -= STALE_PENALTY
            reasons.append('Package not updated in {} days'.format(DAYS_STALE))

    if not no_output:
        score_string = 'score: {}'.format(score)
        print(get_health_color(score)(score_string))

    if verbose and not no_output:
        for reason in reasons:
            print(reason)

    if no_output:
        return score, reasons


def get_health_color(score):
    """
    Returns a color based on the health score
    :param score: integer from 0 - 100 representing health
    :return: string of color to apply in terminal
    """
    color = TERMINAL.green

    if score <= 80:
        color = TERMINAL.yellow
    elif score <= 60:
        color = TERMINAL.orange
    elif score <= 40:
        color = TERMINAL.red

    return color

def main():
    """
    Parses user input for a package name
    :return:
    """
    parser = argparse.ArgumentParser('Determines the health of a package')

    parser.add_argument(
        'package_name',
        help='Name of package listed on pypi.python.org',
    )

    parser.add_argument(
        'package_version', nargs='?',
        help='Version of package to check',
    )

    parser.add_argument(
        '-v', '--verbose', required=False,
        help='Show verbose output - the reasons for the package health score',
        action='store_true'
    )

    parser.add_argument(
        '-n', '--no_output', required=False,
        help='Show verbose output - the reasons for the package health score',
        action='store_true'
    )

    args = parser.parse_args()

    return calculate_health(args.package_name, args.package_version, args.verbose, args.no_output)


if __name__ == '__main__':
    main()
