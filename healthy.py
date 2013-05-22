#! /usr/bin/env python
# coding=utf-8

"""
healthy.py

Checks the health of a Python package, based on it's Pypi information
"""
import argparse
import os
import checks

try:
    # Different location in Python 3
    from xmlrpc.client import ServerProxy
except ImportError:
    from xmlrpclib import ServerProxy

try:
    from blessings import Terminal
except:
    class Terminal(object):
        """A dummy Terminal class if we can't import Terminal."""
        def passthrough(self, s):
            return s
        bold = red = green = yellow = orange = passthrough

TERMINAL = Terminal()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CLIENT = ServerProxy('http://pypi.python.org/pypi')


def calculate_health(package_name, package_version=None, verbose=False, no_output=False):
    """
    Calculates the health of a package, based on several factors

    :param package_name: name of package on pypi.python.org
    :param package_version: version number of package to check, optional - defaults to latest version
    :param verbose: flag to print out reasons
    :param no_output: print no output
    :param lint: run pylint on the package

    :returns: (score: integer, reasons: list of reasons for score)
    :rtype: tuple
    """
    total_score = 0
    reasons = []

    package_releases = CLIENT.package_releases(package_name)
    if not package_releases:
        if not no_output:
            print(TERMINAL.red('{} is not listed on pypi'.format(package_name)))
        return 0, []

    if package_version is None:
        package_version = package_releases[0]

    package_info = CLIENT.release_data(package_name, package_version)
    release_urls = CLIENT.release_urls(package_name, package_version)

    if not no_output:
        print(TERMINAL.bold('{} v{}'.format(package_name, package_version)))
        print('-----')

    checkers = [
        checks.check_license,
        checks.check_homepage,
        checks.check_summary,
        checks.check_description,
        checks.check_python_classifiers,
        checks.check_author_info,
        checks.check_release_files,
        checks.check_stale
    ]

    for checker in checkers:
        result, reason, score = checker(package_info, release_urls)
        if result:
            total_score += score
        else:
            reasons.append(reason)

    if total_score < 0:
        total_score = 0

    if not no_output:
        score_string = 'score: {}/{} {}%'.format(
            total_score, checks.TOTAL_POSSIBLE, int(float(total_score) / float(checks.TOTAL_POSSIBLE) * 100)
        )
        print(get_health_color(total_score)(score_string))

    if verbose and not no_output:
        for reason in reasons:
            print(reason)

    if no_output:
        return total_score, reasons

# def lint_package(download_url):
#     """
#     Run pylint on the packages files
#     :param download_url: download url for the package
#     :return: score of the package
#     """
#     sandbox = create_sandbox()
#     package_dir = download_package_to_sandbox(sandbox, download_url)
#     pylint_score = score(package_dir)
#     destroy_sandbox(sandbox)
#
#     return pylint_score

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
        help='Show no output - no output will be generated',
        action='store_true'
    )

    args = parser.parse_args()

    return calculate_health(args.package_name, args.package_version, args.verbose, args.no_output)


if __name__ == '__main__':
    main()
