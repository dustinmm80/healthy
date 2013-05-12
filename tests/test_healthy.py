#!/usr/bin/env python
# coding=utf-8

"""
Tests for the checkmyreqs package
"""
import unittest
from healthy import calculate_health


class HealthyTestCases(unittest.TestCase):
    """
    Test cases for calculating the health of pypi packages
    """

    def test_package_no_version(self):
        """
        A user has passed in no version
        """
        health, reasons = calculate_health('Django', no_output=True)

        self.assertEqual(health, 100)

        self.assertEqual(len(reasons), 0)

    def test_package_with_version(self):
        """
        A user has passed in a version
        """
        health, reasons = calculate_health('Django', '1.4.1', no_output=True)

        self.assertEqual(health, 70)

        self.assertEqual(len(reasons), 2)

    def test_missing_package(self):
        """
        User passed in a package not on pypi
        """
        health, reasons = calculate_health('j8aj9d8whadjjslkh', '1.4.1', no_output=True)

        self.assertEqual(health, 0)

        self.assertEqual(len(reasons), 0)

if __name__ == '__main__':
    unittest.main()
