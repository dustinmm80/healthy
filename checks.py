#! /usr/bin/env python
# coding=utf-8

"""
checks.py

Check functions that healthy employs to generate a score
"""
from datetime import datetime, timedelta

DAYS_STALE = 180  # number of days without update that a package is considered 'stale'

# Points
HAS_LICENSE             = 20
HAS_RELEASE_FILES       = 30
NOT_STALE               = 15
HAS_SUMMARY             = 15
HAS_DESCRIPTION         = 30
HAS_PYTHON_CLASSIFIERS  = 15
HAS_AUTHOR_INFO         = 10
HAS_HOMEPAGE            = 10

TOTAL_POSSIBLE = sum(
    [
        HAS_LICENSE, HAS_RELEASE_FILES, NOT_STALE, HAS_SUMMARY, HAS_DESCRIPTION, HAS_PYTHON_CLASSIFIERS,
        HAS_AUTHOR_INFO, HAS_HOMEPAGE
    ]
)

BAD_VALUES = ['UNKNOWN', '', None]


def check_license(package_info, *args):
    """
    Does the package have a license classifier?
    :param package_info: package_info dictionary
    :return: Tuple (is the condition True or False?, reason if it is False else None, score to be applied)
    """
    classifiers = package_info.get('classifiers')
    reason = "No License"
    result = False

    if len([c for c in classifiers if c.startswith('License ::')]) > 0:
        result = True

    return result, reason, HAS_LICENSE


def check_homepage(package_info, *args):
    """
    Does the package have a homepage listed?
    :param package_info: package_info dictionary
    :return: Tuple (is the condition True or False?, reason if it is False else None)
    """
    reason = "Home page missing"
    result = False

    if package_info.get('home_page') not in BAD_VALUES:
        result = True

    return result, reason, HAS_HOMEPAGE


def check_summary(package_info, *args):
    """
    Does the package have a summary listed?
    :param package_info: package_info dictionary
    :return: Tuple (is the condition True or False?, reason if it is False else None)
    """
    reason = "Summary missing"
    result = False

    if package_info.get('summary') not in BAD_VALUES:
        result = True

    return result, reason, HAS_SUMMARY


def check_description(package_info, *args):
    """
    Does the package have a description listed?
    :param package_info: package_info dictionary
    :return: Tuple (is the condition True or False?, reason if it is False else None)
    """
    reason = "Description missing"
    result = False

    if package_info.get('description') not in BAD_VALUES:
        result = True

    return result, reason, HAS_DESCRIPTION


def check_python_classifiers(package_info, *args):
    """
    Does the package have Python classifiers?
    :param package_info: package_info dictionary
    :return: Tuple (is the condition True or False?, reason if it is False else None, score to be applied)
    """
    classifiers = package_info.get('classifiers')
    reason = "Python classifiers missing"
    result = False

    if len([c for c in classifiers if c.startswith('Programming Language :: Python ::')]) > 0:
        result = True

    return result, reason, HAS_PYTHON_CLASSIFIERS


def check_author_info(package_info, *args):
    """
    Does the package have author information listed?
    :param package_info: package_info dictionary
    :return: Tuple (is the condition True or False?, reason if it is False else None)
    """
    reason = "Author name or email missing"
    result = False

    if package_info.get('author') not in BAD_VALUES or package_info.get('author_email') not in BAD_VALUES:
        result = True

    return result, reason, HAS_AUTHOR_INFO


def check_release_files(package_info, *args):
    """
    Does the package have release files?
    :param package_info: package_info dictionary
    :return: Tuple (is the condition True or False?, reason if it is False else None)
    """
    reason = "No release files uploaded"
    result = False

    release_urls = args[0]
    if len(release_urls) > 0:
        result = True

    return result, reason, HAS_RELEASE_FILES


def check_stale(package_info, *args):
    """
    Is the package stale?
    :param package_info: package_info dictionary
    :return: Tuple (is the condition True or False?, reason if it is False else None)
    """
    reason = 'Package not updated in {} days'.format(DAYS_STALE)
    result = False

    now = datetime.utcnow()

    release_urls = args[0]
    if len(release_urls) > 0:
        package_uploaded_time = release_urls[0]['upload_time']
        if now - timedelta(days=DAYS_STALE) <= package_uploaded_time:
            result = True

    return result, reason, NOT_STALE
